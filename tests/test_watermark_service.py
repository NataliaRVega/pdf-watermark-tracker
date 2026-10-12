
from pathlib import Path

from pypdf import PdfReader
from reportlab.pdfgen import canvas

from src.pdf_watermark_tracker.models.watermark import Watermark
from src.pdf_watermark_tracker.services.watermark_service import apply_watermarks


def test_apply_text_watermark(tmp_path: Path):
    original_pdf = tmp_path / "original.pdf"
    output_pdf = tmp_path / "watermarked.pdf"

    # Create a small sample PDF with two pages.
    pdf_canvas = canvas.Canvas(str(original_pdf))
    pdf_canvas.drawString(100, 700, "Original page one")
    pdf_canvas.showPage()
    pdf_canvas.drawString(100, 700, "Original page two")
    pdf_canvas.save()

    watermark = Watermark(
        name="Copy code",
        watermark_type="text",
        text="COPY01",
        pages=[2],
        position="bottom_center",
    )

    apply_watermarks(
        input_pdf=original_pdf,
        output_pdf=output_pdf,
        watermarks=[watermark],
    )

    # The original remains available and unchanged in page count.
    assert original_pdf.exists()
    assert len(PdfReader(str(original_pdf)).pages) == 2

    # The new PDF has both pages.
    result = PdfReader(str(output_pdf))
    assert len(result.pages) == 2

    # The watermark should appear on page two, but not page one.
    page_one_text = result.pages[0].extract_text()
    page_two_text = result.pages[1].extract_text()

    assert "COPY01" not in page_one_text
    assert "COPY01" in page_two_text
