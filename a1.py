from typing import List
import os
import fitz  # PyMuPDF

def export_pages_with_images(pdf_path: str, output_dir: str) -> List[str]:
    """
    Scan a PDF and export full-page PNGs (200 DPI) only for pages that contain images.

    Args:
        pdf_path: Path to the input PDF file.
        output_dir: Directory where page images should be saved.

    Returns:
        A list of saved image file paths (one per page that contains at least one image).
        Returns an empty list if no pages contain images.
    """
    os.makedirs(output_dir, exist_ok=True)
    image_paths: List[str] = []

    # Open PDF
    with fitz.open(pdf_path) as doc:
        for page in doc:
            # Detect embedded raster images on the page
            has_images = bool(page.get_images(full=True))
            if not has_images:
                continue

            # Render full page to a pixmap at 200 DPI
            pix = page.get_pixmap(dpi=200)

            # Name like: page_1.png, page_2.png, ...
            filename = f"page_{page.number + 1}.png"

            # Save each image in a path called image_path
            image_path = os.path.join(output_dir, filename)
            pix.save(image_path)

            image_paths.append(image_path)

    return image_paths
