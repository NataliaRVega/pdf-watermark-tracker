
import csv
from datetime import datetime
from pathlib import Path

from src.pdf_watermark_tracker.models.watermark import Watermark
from src.pdf_watermark_tracker.services.watermark_service import apply_watermarks


DEFAULT_FILENAME_PATTERN = "{nombre}_unidad{numero}"


def _create_manifest_path(output_dir: Path) -> Path:
    """Create a unique timestamped manifest filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest_path = output_dir / f"manifest_{timestamp}.csv"

    suffix = 2
    while manifest_path.exists():
        manifest_path = output_dir / f"manifest_{timestamp}_{suffix}.csv"
        suffix += 1

    return manifest_path


def _build_filename(
    pattern: str,
    document_name: str,
    number: int,
    number_padding: int,
) -> str:
    """Build a safe PDF filename from the selected pattern."""
    if not pattern.strip():
        raise ValueError("Filename pattern cannot be empty.")

    if "{nombre}" not in pattern or "{numero}" not in pattern:
        raise ValueError(
            "Filename pattern must include {nombre} and {numero}."
        )

    formatted_number = str(number).zfill(number_padding)

    try:
        filename = pattern.format(
            nombre=document_name,
            numero=formatted_number,
        )
    except (KeyError, ValueError, IndexError) as exc:
        raise ValueError(f"Invalid filename pattern: {pattern}") from exc

    invalid_characters = '<>:"/\\|?*'

    if (
        not filename.strip()
        or filename in {".", ".."}
        or any(char in invalid_characters for char in filename)
        or filename.endswith((" ", "."))
    ):
        raise ValueError(
            f"Pattern generated an invalid filename: {filename}"
        )

    return filename + ".pdf"


def generate_batch(
    input_pdf: str | Path | None = None,
    output_dir: str | Path | None = None,
    copy_count: int = 1,
    code_prefix: str = "COPY",
    watermarks: list[Watermark] | None = None,
    *,
    input_path: str | Path | None = None,
    filename_pattern: str = DEFAULT_FILENAME_PATTERN,
    number_padding: int = 3,
) -> list[Path]:
    """Generate PDF copies and a separate CSV manifest for each batch."""
    source = input_pdf if input_pdf is not None else input_path

    if source is None:
        raise ValueError("An input PDF path is required.")

    if output_dir is None:
        raise ValueError("An output directory is required.")

    source = Path(source)
    output_dir = Path(output_dir)

    if not source.is_file():
        raise FileNotFoundError(f"Input PDF not found: {source}")

    if copy_count < 1:
        raise ValueError("Copy count must be at least 1.")

    if number_padding < 1:
        raise ValueError("Number padding must be at least 1.")

    if watermarks is None:
        watermarks = []

    for watermark in watermarks:
        watermark.validate()

    output_dir.mkdir(parents=True, exist_ok=True)

    document_name = source.stem

    output_paths = [
        output_dir
        / _build_filename(
            filename_pattern,
            document_name,
            number,
            number_padding,
        )
        for number in range(1, copy_count + 1)
    ]

    # Check duplicates within the batch and files from previous batches.
    if len(set(output_paths)) != len(output_paths):
        raise ValueError("Filename pattern produces duplicate filenames.")

    existing = [path for path in output_paths if path.exists()]

    if existing:
        raise FileExistsError(
            f"Output file already exists: {existing[0]}"
        )

    manifest_path = _create_manifest_path(output_dir)
    generated_files = []
    manifest_rows = []

    for number, output_path in enumerate(output_paths, start=1):
        copy_code = output_path.stem
        generated_at = datetime.now().astimezone().isoformat(
            timespec="seconds"
        )

        try:
            apply_watermarks(
                input_pdf=source,
                output_pdf=output_path,
                watermarks=watermarks,
                copy_code=copy_code,
            )

            generated_files.append(output_path)
            status = "success"

        except Exception:
            manifest_rows.append(
                {
                    "copy_code": copy_code,
                    "unit_number": number,
                    "generated_at": generated_at,
                    "input_file": str(source.resolve()),
                    "output_file": str(output_path.resolve()),
                    "status": "failed",
                }
            )

            # Preserve the manifest even if one copy fails.
            with manifest_path.open(
                "w",
                newline="",
                encoding="utf-8-sig",
            ) as csv_file:
                writer = csv.DictWriter(
                    csv_file,
                    fieldnames=[
                        "copy_code",
                        "unit_number",
                        "generated_at",
                        "input_file",
                        "output_file",
                        "status",
                    ],
                )
                writer.writeheader()
                writer.writerows(manifest_rows)

            raise

        manifest_rows.append(
            {
                "copy_code": copy_code,
                "unit_number": number,
                "generated_at": generated_at,
                "input_file": str(source.resolve()),
                "output_file": str(output_path.resolve()),
                "status": status,
            }
        )

    with manifest_path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "copy_code",
                "unit_number",
                "generated_at",
                "input_file",
                "output_file",
                "status",
            ],
        )
        writer.writeheader()
        writer.writerows(manifest_rows)

    return generated_files
