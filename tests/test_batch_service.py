
from pathlib import Path
import csv

import pytest
from pypdf import PdfReader
from reportlab.pdfgen import canvas

from src.pdf_watermark_tracker.models.watermark import Watermark
from src.pdf_watermark_tracker.services.batch_service import generate_batch


def test_generate_batch_creates_sequential_copies(tmp_path: Path):
    original_pdf = tmp_path / "claveles.pdf"
    output_dir = tmp_path / "output"

    pdf_canvas = canvas.Canvas(str(original_pdf))
    pdf_canvas.drawString(100, 700, "Original book")
    pdf_canvas.save()

    watermarks = [
        Watermark(
            name="Copy identifier",
            watermark_type="text",
            text="Code: {copy_code}",
            pages=[1],
            position="bottom_center",
        )
    ]

    files = generate_batch(
        input_pdf=original_pdf,
        output_dir=output_dir,
        copy_count=3,
        watermarks=watermarks,
    )

    assert [path.name for path in files] == [
        "claveles_unidad001.pdf",
        "claveles_unidad002.pdf",
        "claveles_unidad003.pdf",
    ]

    for index, pdf_path in enumerate(files, start=1):
        reader = PdfReader(str(pdf_path))
        text = reader.pages[0].extract_text()
        assert f"claveles_unidad{index:03d}" in text

    manifests = list(output_dir.glob("manifest_*.csv"))
    assert len(manifests) == 1

    with manifests[0].open(
        newline="",
        encoding="utf-8-sig",
    ) as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert len(rows) == 3
    assert [row["copy_code"] for row in rows] == [
        "claveles_unidad001",
        "claveles_unidad002",
        "claveles_unidad003",
    ]
    assert [row["unit_number"] for row in rows] == ["1", "2", "3"]
    assert all(row["status"] == "success" for row in rows)
    assert all(row["input_file"].endswith("claveles.pdf") for row in rows)


def test_custom_filename_pattern(tmp_path: Path):
    original_pdf = tmp_path / "claveles.pdf"
    output_dir = tmp_path / "output"

    pdf_canvas = canvas.Canvas(str(original_pdf))
    pdf_canvas.drawString(100, 700, "Original book")
    pdf_canvas.save()

    files = generate_batch(
        input_pdf=original_pdf,
        output_dir=output_dir,
        copy_count=2,
        filename_pattern="{nombre}_loteA_{numero}",
        number_padding=2,
    )

    assert [path.name for path in files] == [
        "claveles_loteA_01.pdf",
        "claveles_loteA_02.pdf",
    ]


def test_existing_output_is_not_overwritten(tmp_path: Path):
    original_pdf = tmp_path / "claveles.pdf"
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    pdf_canvas = canvas.Canvas(str(original_pdf))
    pdf_canvas.drawString(100, 700, "Original book")
    pdf_canvas.save()

    existing_file = output_dir / "claveles_unidad001.pdf"
    existing_file.write_text("keep this file", encoding="utf-8")

    with pytest.raises(FileExistsError):
        generate_batch(
            input_pdf=original_pdf,
            output_dir=output_dir,
            copy_count=1,
        )

    assert existing_file.read_text(encoding="utf-8") == "keep this file"
