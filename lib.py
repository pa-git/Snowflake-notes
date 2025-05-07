import os, subprocess
from pathlib import Path

def docx_to_pdf_lo(input_path: str, output_dir: str):
    prefix = Path("/ms/dist/fsf/PR0J/libreoffice/4.1.5-1")
    env = os.environ.copy()
    # make sure soffice sees its own libs first
    env["LD_LIBRARY_PATH"] = f"{prefix / 'program'}:{prefix / 'program' / 'lib'}:" + env.get("LD_LIBRARY_PATH", "")
    subprocess.run([
        str(prefix / "program" / "soffice"),
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        input_path
    ], check=True, env=env)

# Usage
docx_to_pdf_lo("../files/contract.docx", "../files")
