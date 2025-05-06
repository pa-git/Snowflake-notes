import subprocess
from pathlib import Path

def docx_to_pdf_custom_libreoffice(input_path: str, output_dir: str):
    soffice = Path("/ms/dist/fsf/PR0J/libreoffice/4.1.5-1/program/soffice")
    subprocess.run([
        str(soffice),
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        input_path
    ], check=True)

# Usage
docx_to_pdf_custom_libreoffice("report.docx", "pdf_outputs")
