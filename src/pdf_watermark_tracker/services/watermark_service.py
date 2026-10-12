
from __future__ import annotations

import io
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from src.pdf_watermark_tracker.models.watermark import Watermark


MARGIN = 36


def _hex_to_rgb(color: str) -> tuple[float, float, float]:
    value = color.lstrip("#")

    if len(value) != 6:
        raise ValueError(f"Invalid hexadecimal color: {color}")

    try:
        return (
            int(value[0:2], 16) / 255,
            int(value[2:4], 16) / 255,
            int(value[4:6], 16) / 255,
        )
    except ValueError as exc:
        raise ValueError(f"Invalid hexadecimal color: {color}") from exc


def _get_position(
    position: str,
    page_width: float,
    page_height: float,
    item_width: float,
    item_height: float,
) -> tuple[float, float]:
    if position.endswith("_left"):
        x = MARGIN
    elif position.endswith("_right"):
        x = page_width - MARGIN - item_width
    else:
        x = (page_width - item_width) / 2

    if position.startswith("top_"):
        y = page_height - MARGIN - item_height
    elif position.startswith("bottom_"):
        y = MARGIN
    else:
        x = (page_width - item_width) / 2
        y = (page_height - item_height) / 2

    return x, y


def _draw_text(pdf_canvas, watermark, page_width, page_height, text):
    font = "Helvetica"
    font_size = watermark.font_size
    text_width = pdf_canvas.stringWidth(text, font, font_size)
    text_height = font_size

    x, y = _get_position(
        watermark.position,
        page_width,
        page_height,
        text_width,
        text_height,
    )

    red, green, blue = _hex_to_rgb(watermark.color)

    pdf_canvas.saveState()
    pdf_canvas.setFont(font, font_size)
    pdf_canvas.setFillColorRGB(red, green, blue)
    pdf_canvas.setFillAlpha(watermark.opacity)

    if watermark.rotation:
        pdf_canvas.translate(x + text_width / 2, y + text_height / 2)
        pdf_canvas.rotate(watermark.rotation)
        pdf_canvas.drawCentredString(0, 0, text)
    elif watermark.position.endswith("_center") or watermark.position == "center":
        pdf_canvas.drawCentredString(x + text_width / 2, y, text)
    else:
        pdf_canvas.drawString(x, y, text)

    pdf_canvas.restoreState()


def _draw_image(pdf_canvas, watermark, page_width, page_height):
    if not watermark.image_path:
        raise ValueError(
            f"Watermark '{watermark.name}' does not have an image path."
        )

    image_path = Path(watermark.image_path)

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    width = watermark.image_width
    height = watermark.image_height

    x, y = _get_position(
        watermark.position,
        page_width,
        page_height,
        width,
        height,
    )

    pdf_canvas.saveState()
    pdf_canvas.setFillAlpha(watermark.opacity)

    if watermark.rotation:
        pdf_canvas.translate(x + width / 2, y + height / 2)
        pdf_canvas.rotate(watermark.rotation)
        x, y = -width / 2, -height / 2

    pdf_canvas.drawImage(
        ImageReader(str(image_path)),
        x,
        y,
        width=width,
        height=height,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )

    pdf_canvas.restoreState()


def _create_overlay(
    page_width,
    page_height,
    watermarks,
    page_number,
    copy_code=None,
):
    buffer = io.BytesIO()
    overlay_canvas = canvas.Canvas(
        buffer,
        pagesize=(page_width, page_height),
    )

    for watermark in watermarks:
        if not watermark.applies_to_page(page_number):
            continue

        watermark.validate()

        if watermark.watermark_type == "text":
            text = watermark.text

            if copy_code:
                text = text.replace("{copy_code}", copy_code)

            _draw_text(
                overlay_canvas,
                watermark,
                page_width,
                page_height,
                text,
            )
        elif watermark.watermark_type == "image":
            _draw_image(
                overlay_canvas,
                watermark,
                page_width,
                page_height,
            )

    overlay_canvas.save()
    buffer.seek(0)

    return PdfReader(buffer)


def create_watermarked_pdf_bytes(
    input_path: str | Path,
    watermarks: list[Watermark],
    copy_code: str | None = None,
) -> bytes:
    """Create a watermarked PDF in memory without modifying the source."""
    input_path = Path(input_path)

    if not input_path.is_file():
        raise FileNotFoundError(f"PDF not found: {input_path}")

    # Build a writer-owned copy so merge_page doesn't modify reader pages.
    writer = PdfWriter(clone_from=str(input_path))

    if writer.is_encrypted:
        raise ValueError("Encrypted PDFs are not supported.")

    for page_number, page in enumerate(writer.pages, start=1):
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)

        applicable = [
            watermark
            for watermark in watermarks
            if watermark.applies_to_page(page_number)
        ]

        if applicable:
            overlay_reader = _create_overlay(
                page_width,
                page_height,
                applicable,
                page_number,
                copy_code,
            )
            page.merge_page(overlay_reader.pages[0])

    output_buffer = io.BytesIO()
    writer.write(output_buffer)

    return output_buffer.getvalue()


def apply_watermarks(
    input_pdf: str | Path | None = None,
    output_pdf: str | Path | None = None,
    watermarks: list[Watermark] | None = None,
    copy_code: str | None = None,
    *,
    input_path: str | Path | None = None,
    output_path: str | Path | None = None,
) -> Path:
    """Apply watermarks and save the result."""
    source = input_pdf if input_pdf is not None else input_path
    destination = output_pdf if output_pdf is not None else output_path

    if source is None:
        raise ValueError("An input PDF path is required.")

    if destination is None:
        raise ValueError("An output PDF path is required.")

    if watermarks is None:
        watermarks = []

    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    pdf_bytes = create_watermarked_pdf_bytes(
        input_path=source,
        watermarks=watermarks,
        copy_code=copy_code,
    )

    destination.write_bytes(pdf_bytes)
    return destination
