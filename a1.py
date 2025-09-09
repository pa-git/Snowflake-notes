from typing import List, Tuple
import os
import fitz  # PyMuPDF

def export_pages_with_images(pdf_path: str, output_dir: str) -> Tuple[List[int], List[str]]:
    """
    Scan a PDF and export full-page PNGs (200 DPI) only for pages that contain images.

    Args:
        pdf_path: Path to the input PDF file.
        output_dir: Directory where page images should be saved.

    Returns:
        A tuple of (page_indices_with_images, image_paths):
          - page_indices_with_images: 0-based indices of pages that contain at least one embedded raster image
          - image_paths: file paths to the saved PNGs (named page_1.png, page_2.png, ...)
        Returns ([], []) if no pages contain images.
    """
    os.makedirs(output_dir, exist_ok=True)
    page_indices_with_images: List[int] = []
    image_paths: List[str] = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            # Detect embedded raster images on the page
            if not page.get_images(full=True):
                continue

            page_indices_with_images.append(page.number)  # 0-based index

            # Render full page to a pixmap at 200 DPI
            pix = page.get_pixmap(dpi=200)

            # Human-friendly 1-based naming: page_1.png, page_2.png, ...
            filename = f"page_{page.number + 1}.png"
            image_path = os.path.join(output_dir, filename)
            pix.save(image_path)
            image_paths.append(image_path)

    return page_indices_with_images, image_paths
