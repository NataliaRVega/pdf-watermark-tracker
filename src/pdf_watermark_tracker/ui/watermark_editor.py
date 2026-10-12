
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk

from src.pdf_watermark_tracker.models.watermark import Watermark


POSITIONS = [
    "top_left",
    "top_center",
    "top_right",
    "center",
    "bottom_left",
    "bottom_center",
    "bottom_right",
]


class WatermarkEditor(ctk.CTkFrame):
    def __init__(self, master, translate, language="es", **kwargs):
        super().__init__(master, **kwargs)

        self.translate = translate
        self.language = language
        self.items = []

        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=8, pady=8)

        self.title_label = ctk.CTkLabel(
            self.header,
            text=self.t("watermarks"),
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.title_label.pack(side="left")

        self.add_button = ctk.CTkButton(
            self.header,
            text=self.t("add_watermark"),
            command=self.add_watermark,
            width=160,
        )
        self.add_button.pack(side="right")

        self.items_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.items_frame.pack(fill="x", padx=4, pady=(0, 8))

        self.add_watermark()

    def t(self, key):
        return self.translate(key, self.language)

    def set_language(self, language):
        self.language = language
        self.title_label.configure(text=self.t("watermarks"))
        self.add_button.configure(text=self.t("add_watermark"))

        for item in self.items:
            self._translate_item(item)

    def add_watermark(self):
        item = {}
        item["frame"] = ctk.CTkFrame(self.items_frame)
        item["frame"].pack(fill="x", padx=4, pady=6)

        header = ctk.CTkFrame(item["frame"], fg_color="transparent")
        header.pack(fill="x", padx=8, pady=(8, 4))

        item["name_label"] = ctk.CTkLabel(header, text=self.t("name"))
        item["name_label"].pack(side="left")

        item["name"] = ctk.CTkEntry(header, width=140)
        item["name"].insert(0, f"Watermark {len(self.items) + 1}")
        item["name"].pack(side="left", padx=6)

        item["type"] = ctk.CTkOptionMenu(
            header,
            values=["text", "image"],
            command=lambda value, current=item: self._set_type(current, value),
            width=100,
        )
        item["type"].set("text")
        item["type"].pack(side="left", padx=6)

        item["remove_button"] = ctk.CTkButton(
            header,
            text=self.t("remove"),
            width=80,
            fg_color="#9b3434",
            hover_color="#7d2929",
            command=lambda current=item: self.remove_watermark(current),
        )
        item["remove_button"].pack(side="right")

        item["text_row"] = ctk.CTkFrame(item["frame"], fg_color="transparent")
        item["text_row"].pack(fill="x", padx=8, pady=4)

        item["text_label"] = ctk.CTkLabel(
            item["text_row"],
            text=self.t("text"),
            width=80,
        )
        item["text_label"].pack(side="left")

        item["text"] = ctk.CTkEntry(
            item["text_row"],
            placeholder_text="Confidential / {copy_code}",
        )
        item["text"].pack(side="left", fill="x", expand=True)

        item["image_row"] = ctk.CTkFrame(item["frame"], fg_color="transparent")
        item["image_label"] = ctk.CTkLabel(
            item["image_row"],
            text=self.t("image"),
            width=80,
        )
        item["image_label"].pack(side="left")

        item["image_path"] = ctk.CTkEntry(item["image_row"])
        item["image_path"].pack(side="left", fill="x", expand=True, padx=4)

        item["image_button"] = ctk.CTkButton(
            item["image_row"],
            text=self.t("choose_image"),
            width=130,
            command=lambda current=item: self._choose_image(current),
        )
        item["image_button"].pack(side="right")

        item["pages_row"] = ctk.CTkFrame(item["frame"], fg_color="transparent")
        item["pages_row"].pack(fill="x", padx=8, pady=4)

        item["pages_label"] = ctk.CTkLabel(
            item["pages_row"],
            text=self.t("pages"),
        )
        item["pages_label"].pack(side="left")

        item["pages_entry"] = ctk.CTkEntry(item["pages_row"])
        item["pages_entry"].pack(side="left", fill="x", expand=True, padx=6)

        item["settings_row"] = ctk.CTkFrame(item["frame"], fg_color="transparent")
        item["settings_row"].pack(fill="x", padx=8, pady=4)

        item["position_label"] = ctk.CTkLabel(
            item["settings_row"],
            text=self.t("position"),
        )
        item["position_label"].pack(side="left")

        item["position"] = ctk.CTkOptionMenu(
            item["settings_row"],
            values=POSITIONS,
            width=135,
        )
        item["position"].set("bottom_center")
        item["position"].pack(side="left", padx=5)

        item["opacity_label"] = ctk.CTkLabel(
            item["settings_row"],
            text=self.t("opacity"),
        )
        item["opacity_label"].pack(side="left", padx=(8, 2))

        item["opacity"] = ctk.CTkEntry(item["settings_row"], width=55)
        item["opacity"].insert(0, "0.7")
        item["opacity"].pack(side="left", padx=4)

        item["rotation_label"] = ctk.CTkLabel(
            item["settings_row"],
            text=self.t("rotation"),
        )
        item["rotation_label"].pack(side="left", padx=(8, 2))

        item["rotation"] = ctk.CTkEntry(item["settings_row"], width=55)
        item["rotation"].insert(0, "0")
        item["rotation"].pack(side="left", padx=4)

        item["font_row"] = ctk.CTkFrame(item["frame"], fg_color="transparent")
        item["font_label"] = ctk.CTkLabel(
            item["font_row"],
            text=self.t("font_size"),
            width=100,
        )
        item["font_label"].pack(side="left")

        item["font_size"] = ctk.CTkEntry(item["font_row"], width=70)
        item["font_size"].insert(0, "16")
        item["font_size"].pack(side="left", padx=4)

        item["image_size_row"] = ctk.CTkFrame(
            item["frame"],
            fg_color="transparent",
        )

        item["image_width_label"] = ctk.CTkLabel(
            item["image_size_row"],
            text=self.t("image_width"),
        )
        item["image_width_label"].pack(side="left")

        item["image_width"] = ctk.CTkEntry(item["image_size_row"], width=70)
        item["image_width"].insert(0, "100")
        item["image_width"].pack(side="left", padx=4)

        item["image_height_label"] = ctk.CTkLabel(
            item["image_size_row"],
            text=self.t("image_height"),
        )
        item["image_height_label"].pack(side="left", padx=(8, 0))

        item["image_height"] = ctk.CTkEntry(item["image_size_row"], width=70)
        item["image_height"].insert(0, "60")
        item["image_height"].pack(side="left", padx=4)

        self.items.append(item)
        self._set_type(item, "text")

    def _translate_item(self, item):
        item["name_label"].configure(text=self.t("name"))
        item["remove_button"].configure(text=self.t("remove"))
        item["text_label"].configure(text=self.t("text"))
        item["image_label"].configure(text=self.t("image"))
        item["image_button"].configure(text=self.t("choose_image"))
        item["pages_label"].configure(text=self.t("pages"))
        item["position_label"].configure(text=self.t("position"))
        item["opacity_label"].configure(text=self.t("opacity"))
        item["rotation_label"].configure(text=self.t("rotation"))
        item["font_label"].configure(text=self.t("font_size"))
        item["image_width_label"].configure(text=self.t("image_width"))
        item["image_height_label"].configure(text=self.t("image_height"))

    def _set_type(self, item, value):
        item["text_row"].pack_forget()
        item["image_row"].pack_forget()
        item["font_row"].pack_forget()
        item["image_size_row"].pack_forget()

        if value == "image":
            item["image_row"].pack(
                fill="x",
                padx=8,
                pady=4,
                before=item["pages_row"],
            )
            item["image_size_row"].pack(fill="x", padx=8, pady=4)
        else:
            item["text_row"].pack(
                fill="x",
                padx=8,
                pady=4,
                before=item["pages_row"],
            )
            item["font_row"].pack(fill="x", padx=8, pady=4)

    def _choose_image(self, item):
        path = filedialog.askopenfilename(
            title=self.t("choose_image"),
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp"),
                ("All files", "*.*"),
            ],
        )

        if path:
            item["image_path"].delete(0, tk.END)
            item["image_path"].insert(0, path)

    def remove_watermark(self, item):
        item["frame"].destroy()
        self.items.remove(item)

    @staticmethod
    def _parse_pages(value):
        """Parse page specifications such as '1,3-5'."""
        value = value.strip()

        if not value:
            return []

        pages = set()

        for part in value.split(","):
            part = part.strip()

            if "-" in part:
                start_text, end_text = part.split("-", maxsplit=1)
                start = int(start_text.strip())
                end = int(end_text.strip())

                if end < start:
                    raise ValueError(f"Invalid page range: {part}")

                pages.update(range(start, end + 1))
            else:
                pages.add(int(part))

        return sorted(pages)

    def get_watermarks(self):
        watermarks = []

        for item in self.items:
            watermark_type = item["type"].get()
            pages = self._parse_pages(item["pages_entry"].get())

            watermark = Watermark(
                name=item["name"].get().strip() or "Watermark",
                watermark_type=watermark_type,
                pages=pages,
                position=item["position"].get(),
                text=item["text"].get(),
                font_size=int(item["font_size"].get()),
                image_path=item["image_path"].get().strip() or None,
                opacity=float(item["opacity"].get()),
                image_width=float(item["image_width"].get()),
                image_height=float(item["image_height"].get()),
                rotation=float(item["rotation"].get()),
            )

            watermark.validate()
            watermarks.append(watermark)

        return watermarks
