
TRANSLATIONS = {
    "app_title": {
        "es": "PDF Watermark Tracker — codigo by natty",
        "en": "PDF Watermark Tracker — codigo by natty",
    },
    "language": {"es": "Idioma", "en": "Language"},
    "input_pdf": {"es": "PDF original", "en": "Input PDF"},
    "choose_pdf": {"es": "Seleccionar PDF", "en": "Choose PDF"},
    "output_folder": {"es": "Carpeta de salida", "en": "Output folder"},
    "choose_folder": {"es": "Seleccionar carpeta", "en": "Choose folder"},
    "copy_count": {"es": "Cantidad de copias", "en": "Number of copies"},
    "code_prefix": {"es": "Prefijo del código", "en": "Code prefix"},
    "watermarks": {"es": "Marcas de agua", "en": "Watermarks"},
    "add_watermark": {"es": "+ Agregar marca", "en": "+ Add watermark"},
    "name": {"es": "Nombre", "en": "Name"},
    "type": {"es": "Tipo", "en": "Type"},
    "text": {"es": "Texto", "en": "Text"},
    "image": {"es": "Imagen", "en": "Image"},
    "choose_image": {"es": "Seleccionar imagen", "en": "Choose image"},
    "pages": {
        "es": "Páginas (vacío = todas; ej. 1,3-5)",
        "en": "Pages (blank = all; e.g. 1,3-5)",
    },
    "position": {"es": "Posición", "en": "Position"},
    "opacity": {"es": "Opacidad (0–1)", "en": "Opacity (0–1)"},
    "font_size": {"es": "Tamaño de fuente", "en": "Font size"},
    "image_width": {"es": "Ancho", "en": "Width"},
    "image_height": {"es": "Alto", "en": "Height"},
    "rotation": {"es": "Rotación", "en": "Rotation"},
    "remove": {"es": "Eliminar", "en": "Remove"},
    "preview": {"es": "Vista previa", "en": "Preview"},
    "refresh_preview": {
        "es": "Actualizar vista previa",
        "en": "Refresh preview",
    },
    "previous": {"es": "Anterior", "en": "Previous"},
    "next": {"es": "Siguiente", "en": "Next"},
    "generate": {
        "es": "Generar copias PDF",
        "en": "Generate PDF copies",
    },
    "select_pdf_first": {
        "es": "Seleccioná un PDF antes de continuar.",
        "en": "Select a PDF before continuing.",
    },
    "select_output_first": {
        "es": "Seleccioná una carpeta de salida.",
        "en": "Select an output folder.",
    },
    "success": {
        "es": "Copias generadas correctamente.",
        "en": "Copies generated successfully.",
    },
    "error": {"es": "Error", "en": "Error"},
    "success_title": {"es": "Proceso completado", "en": "Completed"},
    "no_preview": {
        "es": "Seleccioná un PDF para ver la vista previa.",
        "en": "Select a PDF to preview it.",
    },
    "page": {"es": "Página", "en": "Page"},
}


def translate(key: str, language: str = "es") -> str:
    """Return the translated string or the key as a fallback."""
    return TRANSLATIONS.get(key, {}).get(
        language,
        TRANSLATIONS.get(key, {}).get("es", key),
    )
