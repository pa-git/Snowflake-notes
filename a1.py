import os
import shutil

# Delete if it exists
if os.path.exists(pdf_output_dir):
    shutil.rmtree(pdf_output_dir)

# Recreate with specific permissions
os.makedirs(pdf_output_dir, mode=0o755)
