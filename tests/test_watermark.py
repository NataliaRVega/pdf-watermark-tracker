
from src.pdf_watermark_tracker.models.watermark import Watermark


def test_watermark_applies_to_selected_pages():
    watermark = Watermark(
        name="Illustration",
        watermark_type="image",
        image_path="assets/example.png",
        pages=[20, 100],
    )

    assert watermark.applies_to_page(20)
    assert watermark.applies_to_page(100)
    assert not watermark.applies_to_page(1)


def test_empty_pages_means_all_pages():
    watermark = Watermark(
        name="Copy code",
        watermark_type="text",
        text="COPY01",
    )

    assert watermark.applies_to_page(1)
    assert watermark.applies_to_page(20)
    assert watermark.applies_to_page(100)
