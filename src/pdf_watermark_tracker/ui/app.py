from io import BytesIO
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk
import pymupdf
from PIL import Image

from src.pdf_watermark_tracker.services.batch_service import (
    DEFAULT_FILENAME_PATTERN,
    generate_batch,
)
from src.pdf_watermark_tracker.services.watermark_service import (
    create_watermarked_pdf_bytes,
)
from src.pdf_watermark_tracker.ui.translations import translate
from src.pdf_watermark_tracker.ui.watermark_editor import WatermarkEditor


class PDFWatermarkTrackerApp(ctk.CTk):
    """Desktop application for creating watermarked PDF copies."""

    def __init__(self):
        super().__init__()

        self.title("PDF Watermark Tracker — codigo by natty")
        self.geometry("1100x850")
        self.minsize(850, 700)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Application state
        self.language = tk.StringVar(value="es")
        self.input_pdf = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.copy_count = tk.StringVar(value="5")
        self.code_prefix = tk.StringVar(value="COPY")

        # Filename customization
        self.filename_pattern = tk.StringVar(
            value=DEFAULT_FILENAME_PATTERN
        )
        self.number_padding = tk.StringVar(value="3")

        # PDF preview state
        self.preview_page = 0
        self.preview_photo = None
        self.preview_page_count = 0

        self._build_ui()
        self._translate_widgets()

    # ---------------------------------------------------------
    # Translation helper
    # ---------------------------------------------------------

    def t(self, key):
        """Translate a key using the currently selected language."""
        return translate(key, self.language.get())

    # ---------------------------------------------------------
    # Main interface
    # ---------------------------------------------------------

    def _build_ui(self):
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

        self.main_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
        )
        self.header_frame.pack(fill="x", pady=(0, 12))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="PDF Watermark Tracker",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        self.title_label.pack(side="left", padx=(0, 10))

        self.brand_label = ctk.CTkLabel(
            self.header_frame,
            text="codigo by natty",
            text_color="gray",
            font=ctk.CTkFont(size=12),
        )
        self.brand_label.pack(side="left", pady=(10, 0))

        self.language_menu = ctk.CTkOptionMenu(
            self.header_frame,
            values=["Español", "English"],
            command=self._change_language,
            width=120,
        )
        self.language_menu.set("Español")
        self.language_menu.pack(side="right")

        # Input PDF
        self.input_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
        )
        self.input_frame.pack(fill="x", pady=5)

        self.input_label = ctk.CTkLabel(
            self.input_frame,
            text="PDF de entrada",
            width=150,
            anchor="w",
        )
        self.input_label.pack(side="left")

        self.input_entry = ctk.CTkEntry(
            self.input_frame,
            textvariable=self.input_pdf,
        )
        self.input_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8,
        )

        self.input_button = ctk.CTkButton(
            self.input_frame,
            text="Examinar",
            width=110,
            command=self._browse_input,
        )
        self.input_button.pack(side="right")

        # Output directory
        self.output_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
        )
        self.output_frame.pack(fill="x", pady=5)

        self.output_label = ctk.CTkLabel(
            self.output_frame,
            text="Carpeta de salida",
            width=150,
            anchor="w",
        )
        self.output_label.pack(side="left")

        self.output_entry = ctk.CTkEntry(
            self.output_frame,
            textvariable=self.output_dir,
        )
        self.output_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8,
        )

        self.output_button = ctk.CTkButton(
            self.output_frame,
            text="Examinar",
            width=110,
            command=self._browse_output,
        )
        self.output_button.pack(side="right")

        # Copy count and legacy code prefix
        self.options_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
        )
        self.options_frame.pack(fill="x", pady=5)

        self.copy_count_label = ctk.CTkLabel(
            self.options_frame,
            text="Cantidad de copias",
            width=150,
            anchor="w",
        )
        self.copy_count_label.pack(side="left")

        self.copy_count_entry = ctk.CTkEntry(
            self.options_frame,
            textvariable=self.copy_count,
            width=100,
        )
        self.copy_count_entry.pack(side="left", padx=8)

        self.code_prefix_label = ctk.CTkLabel(
            self.options_frame,
            text="Prefijo de código",
        )
        self.code_prefix_label.pack(side="left", padx=(15, 0))

        self.code_prefix_entry = ctk.CTkEntry(
            self.options_frame,
            textvariable=self.code_prefix,
            width=120,
        )
        self.code_prefix_entry.pack(side="left", padx=8)

        # Filename customization
        self.naming_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
        )
        self.naming_frame.pack(fill="x", pady=6)

        self.filename_pattern_label = ctk.CTkLabel(
            self.naming_frame,
            text="Patrón de nombre",
            width=150,
            anchor="w",
        )
        self.filename_pattern_label.grid(
            row=0,
            column=0,
            padx=(0, 8),
            pady=5,
            sticky="w",
        )

        self.filename_pattern_entry = ctk.CTkEntry(
            self.naming_frame,
            textvariable=self.filename_pattern,
        )
        self.filename_pattern_entry.grid(
            row=0,
            column=1,
            padx=8,
            pady=5,
            sticky="ew",
        )

        self.filename_pattern_help = ctk.CTkLabel(
            self.naming_frame,
            text=(
                "{nombre} = PDF original; "
                "{numero} = número de copia"
            ),
            text_color="gray",
            anchor="w",
            wraplength=600,
        )
        self.filename_pattern_help.grid(
            row=1,
            column=1,
            padx=8,
            pady=(0, 5),
            sticky="w",
        )

        self.number_padding_label = ctk.CTkLabel(
            self.naming_frame,
            text="Dígitos de numeración",
            width=150,
            anchor="w",
        )
        self.number_padding_label.grid(
            row=2,
            column=0,
            padx=(0, 8),
            pady=5,
            sticky="w",
        )

        self.number_padding_menu = ctk.CTkOptionMenu(
            self.naming_frame,
            values=["1", "2", "3"],
            variable=self.number_padding,
            width=100,
        )
        self.number_padding_menu.grid(
            row=2,
            column=1,
            padx=8,
            pady=5,
            sticky="w",
        )

        self.naming_frame.grid_columnconfigure(1, weight=1)

        # Watermark editor
        self.watermark_editor = WatermarkEditor(
            self.main_frame,
            translate=translate,
            language=self.language.get(),
        )
        self.watermark_editor.pack(
            fill="x",
            pady=8,
        )

        # PDF preview section
        self.preview_section = ctk.CTkFrame(self.main_frame)
        self.preview_section.pack(
            fill="both",
            expand=True,
            pady=(8, 10),
        )

        self.preview_title = ctk.CTkLabel(
            self.preview_section,
            text="Vista previa",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.preview_title.pack(pady=(10, 5))

        self.preview_container = ctk.CTkFrame(
            self.preview_section,
            fg_color=("gray90", "gray20"),
        )
        self.preview_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5,
        )

        self.preview_label = ctk.CTkLabel(
            self.preview_container,
            text="Seleccioná un PDF para ver la vista previa.",
        )
        self.preview_label.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10,
        )

        # Preview navigation
        self.preview_controls = ctk.CTkFrame(
            self.preview_section,
            fg_color="transparent",
        )
        self.preview_controls.pack(
            fill="x",
            padx=10,
            pady=(0, 8),
        )

        self.previous_button = ctk.CTkButton(
            self.preview_controls,
            text="Anterior",
            width=110,
            command=self._previous_preview_page,
        )
        self.previous_button.pack(side="left")

        self.preview_page_label = ctk.CTkLabel(
            self.preview_controls,
            text="Página 0 de 0",
        )
        self.preview_page_label.pack(
            side="left",
            expand=True,
        )

        self.next_button = ctk.CTkButton(
            self.preview_controls,
            text="Siguiente",
            width=110,
            command=self._next_preview_page,
        )
        self.next_button.pack(side="right")

        # Preview refresh
        self.preview_button = ctk.CTkButton(
            self.main_frame,
            text="Actualizar vista previa",
            command=self._show_preview,
        )
        self.preview_button.pack(
            fill="x",
            pady=(0, 8),
        )

        # Batch generation
        self.generate_button = ctk.CTkButton(
            self.main_frame,
            text="Generar copias",
            height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._generate_batch,
        )
        self.generate_button.pack(fill="x")

    # ---------------------------------------------------------
    # Language
    # ---------------------------------------------------------

    def _change_language(self, selected_language):
        self.language.set(
            "es" if selected_language == "Español" else "en"
        )
        self._translate_widgets()

    def _translate_widgets(self):
        is_spanish = self.language.get() == "es"

        self.title_label.configure(
            text="PDF Watermark Tracker"
        )

        self.input_label.configure(
            text="PDF de entrada" if is_spanish else "Input PDF"
        )

        self.output_label.configure(
            text="Carpeta de salida"
            if is_spanish
            else "Output folder"
        )

        self.input_button.configure(
            text="Examinar" if is_spanish else "Browse"
        )

        self.output_button.configure(
            text="Examinar" if is_spanish else "Browse"
        )

        self.copy_count_label.configure(
            text="Cantidad de copias"
            if is_spanish
            else "Number of copies"
        )

        self.code_prefix_label.configure(
            text="Prefijo de código"
            if is_spanish
            else "Code prefix"
        )

        self.filename_pattern_label.configure(
            text="Patrón de nombre"
            if is_spanish
            else "Filename pattern"
        )

        self.filename_pattern_help.configure(
            text=(
                "{nombre} = PDF original; "
                "{numero} = número de copia"
                if is_spanish
                else "{nombre} = original PDF; "
                "{numero} = copy number"
            )
        )

        self.number_padding_label.configure(
            text=(
                "Dígitos de numeración"
                if is_spanish
                else "Number of digits"
            )
        )

        self.preview_title.configure(
            text="Vista previa" if is_spanish else "Preview"
        )

        self.preview_button.configure(
            text=(
                "Actualizar vista previa"
                if is_spanish
                else "Refresh preview"
            )
        )

        self.generate_button.configure(
            text="Generar copias"
            if is_spanish
            else "Generate copies"
        )

        self.previous_button.configure(
            text="Anterior" if is_spanish else "Previous"
        )

        self.next_button.configure(
            text="Siguiente" if is_spanish else "Next"
        )

        self.watermark_editor.set_language(self.language.get())
        self._update_preview_page_label()

    # ---------------------------------------------------------
    # File selection
    # ---------------------------------------------------------

    def _browse_input(self):
        selected_file = filedialog.askopenfilename(
            title=(
                "Seleccionar PDF"
                if self.language.get() == "es"
                else "Select PDF"
            ),
            filetypes=[
                ("PDF files", "*.pdf"),
                ("All files", "*.*"),
            ],
        )

        if selected_file:
            self.input_pdf.set(selected_file)
            self.preview_page = 0
            self._show_preview()

    def _browse_output(self):
        selected_dir = filedialog.askdirectory(
            title=(
                "Seleccionar carpeta de salida"
                if self.language.get() == "es"
                else "Select output folder"
            )
        )

        if selected_dir:
            self.output_dir.set(selected_dir)

    # ---------------------------------------------------------
    # PDF preview
    # ---------------------------------------------------------

    def _show_preview(self):
        input_path = self.input_pdf.get().strip()

        if not input_path:
            self.preview_label.configure(
                text=(
                    "Seleccioná un PDF para ver la vista previa."
                    if self.language.get() == "es"
                    else "Select a PDF to see the preview."
                ),
                image=None,
            )
            self.preview_photo = None
            self.preview_page_count = 0
            self._update_preview_page_label()
            return

        try:
            source = Path(input_path)

            if not source.is_file():
                raise FileNotFoundError(
                    f"PDF not found: {input_path}"
                )

            watermarks = self.watermark_editor.get_watermarks()

            document_name = source.stem
            padding = int(self.number_padding.get())

            preview_code = self.filename_pattern.get().format(
                nombre=document_name,
                numero=str(1).zfill(padding),
            )

            preview_bytes = create_watermarked_pdf_bytes(
                input_path=input_path,
                watermarks=watermarks,
                copy_code=preview_code,
            )

            with pymupdf.open(
                stream=preview_bytes,
                filetype="pdf",
            ) as document:
                self.preview_page_count = len(document)

                if self.preview_page_count == 0:
                    raise ValueError("The PDF contains no pages.")

                self.preview_page = min(
                    max(self.preview_page, 0),
                    self.preview_page_count - 1,
                )

                page = document.load_page(self.preview_page)
                pixmap = page.get_pixmap(
                    matrix=pymupdf.Matrix(1.2, 1.2),
                    alpha=False,
                )

                image_bytes = pixmap.tobytes("png")

            with Image.open(BytesIO(image_bytes)) as image:
                preview_image = image.copy()

            # Keep the image within a reasonable preview size.
            preview_image.thumbnail((650, 650))

            self.preview_photo = ctk.CTkImage(
                light_image=preview_image,
                dark_image=preview_image,
                size=preview_image.size,
            )

            self.preview_label.configure(
                image=self.preview_photo,
                text="",
            )

            self._update_preview_page_label()

        except Exception as exc:
            self.preview_photo = None
            self.preview_page_count = 0

            prefix = (
                "Error en la vista previa"
                if self.language.get() == "es"
                else "Preview error"
            )

            self.preview_label.configure(
                image=None,
                text=f"{prefix}:\n{exc}",
            )

            self._update_preview_page_label()

    def _previous_preview_page(self):
        if self.preview_page > 0:
            self.preview_page -= 1
            self._show_preview()

    def _next_preview_page(self):
        if self.preview_page < self.preview_page_count - 1:
            self.preview_page += 1
            self._show_preview()

    def _update_preview_page_label(self):
        is_spanish = self.language.get() == "es"

        if self.preview_page_count == 0:
            text = (
                "Página 0 de 0"
                if is_spanish
                else "Page 0 of 0"
            )
        else:
            text = (
                f"Página {self.preview_page + 1} "
                f"de {self.preview_page_count}"
                if is_spanish
                else f"Page {self.preview_page + 1} "
                f"of {self.preview_page_count}"
            )

        self.preview_page_label.configure(text=text)

        self.previous_button.configure(
            state=(
                "normal"
                if self.preview_page > 0
                else "disabled"
            )
        )

        self.next_button.configure(
            state=(
                "normal"
                if self.preview_page < self.preview_page_count - 1
                else "disabled"
            )
        )

    # ---------------------------------------------------------
    # Batch generation
    # ---------------------------------------------------------

    def _generate_batch(self):
        input_path = self.input_pdf.get().strip()
        output_dir = self.output_dir.get().strip()

        is_spanish = self.language.get() == "es"

        if not input_path:
            messagebox.showwarning(
                self.t("error"),
                self.t("select_pdf_first"),
            )
            return

        if not output_dir:
            messagebox.showwarning(
                self.t("error"),
                self.t("select_output_first"),
            )
            return

        try:
            copies = int(self.copy_count.get())
            padding = int(self.number_padding.get())
            pattern = self.filename_pattern.get().strip()

            if copies < 1:
                raise ValueError(
                    "La cantidad de copias debe ser al menos 1."
                    if is_spanish
                    else "The number of copies must be at least 1."
                )

            if padding < 1:
                raise ValueError(
                    "La numeración debe tener al menos un dígito."
                    if is_spanish
                    else "Number padding must be at least 1."
                )

            if not pattern:
                raise ValueError(
                    "El patrón de nombre no puede estar vacío."
                    if is_spanish
                    else "The filename pattern cannot be empty."
                )

            watermarks = self.watermark_editor.get_watermarks()

            generated = generate_batch(
                input_path=input_path,
                output_dir=output_dir,
                copy_count=copies,
                code_prefix=self.code_prefix.get(),
                watermarks=watermarks,
                filename_pattern=pattern,
                number_padding=padding,
            )

            # Locate the newest timestamped manifest.
            manifests = sorted(
                Path(output_dir).glob("manifest_*.csv"),
                key=lambda path: path.stat().st_mtime,
                reverse=True,
            )

            manifest_message = (
                str(manifests[0])
                if manifests
                else (
                    "No se encontró el manifiesto."
                    if is_spanish
                    else "Manifest not found."
                )
            )

            messagebox.showinfo(
                self.t("success_title"),
                (
                    f"{self.t('success')}\n\n"
                    f"{len(generated)} PDF(s)\n"
                    f"{manifest_message}"
                ),
            )

        except Exception as exc:
            messagebox.showerror(
                self.t("error"),
                str(exc),
            )


# Compatibility aliases in case main.py imports a shorter class name.
App = PDFWatermarkTrackerApp
WatermarkTrackerApp = PDFWatermarkTrackerApp


def run_app():
    """Create and run the application."""
    app = PDFWatermarkTrackerApp()
    app.mainloop()


if __name__ == "__main__":
    run_app()
