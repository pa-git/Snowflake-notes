#!/usr/bin/env python3
import os
import argparse
import subprocess

def convert_md_to_pdf(input_file, output_file):
    """Convert a Markdown file to a PDF using pandoc at a custom path."""
    # Provide the absolute path to pandoc here:
    pandoc_path = "/apps/x86_64/pandoc/2.9/bin/pandoc.exe"

    try:
        subprocess.run([pandoc_path, input_file, "-o", output_file], check=True)
        print(f"Converted: {input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file}: {e}")

def main(folder):
    """Process all Markdown files in the given folder."""
    if not os.path.isdir(folder):
        print(f"Error: The folder '{folder}' does not exist.")
        return

    for filename in os.listdir(folder):
        if filename.lower().endswith(".md"):
            input_path = os.path.join(folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".pdf"
            output_path = os.path.join(folder, output_filename)
            convert_md_to_pdf(input_path, output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert Markdown files to PDF.")
    parser.add_argument("folder", nargs="?", default=".", help="Folder containing .md files (default: current dir).")
    args = parser.parse_args()
    main(args.folder)
