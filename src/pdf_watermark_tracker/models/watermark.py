
from dataclasses import dataclass, field
from typing import Literal


Position = Literal[
    "top_left",
    "top_center",
    "top_right",
    "center",
    "bottom_left",
    "bottom_center",
    "bottom_right",
]


@dataclass
class Watermark:
    """Configuration for a text or image watermark."""

    name: str
    watermark_type: Literal["text", "image"]

    # Empty list means all pages.
    pages: list[int] = field(default_factory=list)
    position: Position = "bottom_center"

    # Text settings
    text: str = ""
    font_size: int = 10
    color: str = "#666666"

    # Image settings, in PDF points
    image_path: str | None = None
    image_width: float = 60
    image_height: float = 60

    opacity: float = 0.7
    rotation: float = 0

    def applies_to_page(self, page_number: int) -> bool:
        """Check whether this watermark applies to a 1-based page number."""
        return not self.pages or page_number in self.pages

    def validate(self) -> None:
        """Validate this watermark configuration."""
        if self.watermark_type not in ("text", "image"):
            raise ValueError("Watermark type must be 'text' or 'image'.")

        if self.watermark_type == "text" and not self.text.strip():
            raise ValueError("Text watermark cannot be empty.")

        if self.watermark_type == "image":
            if not self.image_path:
                raise ValueError("Image watermark requires an image path.")

        if any(page < 1 for page in self.pages):
            raise ValueError("Page numbers must be greater than zero.")

        if self.font_size < 1:
            raise ValueError("Font size must be positive.")

        if not 0 <= self.opacity <= 1:
            raise ValueError("Opacity must be between 0 and 1.")

        if self.image_width <= 0 or self.image_height <= 0:
            raise ValueError("Image dimensions must be positive.")
