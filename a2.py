import os
from datetime import datetime

# Dummy kickof function for illustration
def kickof(filename):
    # Replace this with your actual logic
    if "fail" in filename.lower():
        raise ValueError("Simulated failure")
    print(f"Processing {filename}")

def process_pdf_files(folder_path, markdown_folder="markdown"):
    # Prepare logs folder and log file
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = f"logs/process_log_{timestamp}.txt"

    try:
        log_file = open(log_file_path, "w", encoding="utf-8")
    except Exception as e:
        print(f"Unable to open log file: {e}")
        return

    # Get base names of markdown files (without extension)
    md_basenames = set()
    if os.path.exists(markdown_folder):
        for md_file in os.listdir(markdown_folder):
            if md_file.lower().endswith(".md"):
                base_name = os.path.splitext(md_file)[0]
                md_basenames.add(base_name)

    try:
        files = os.listdir(folder_path)
    except Exception as e:
        log_file.write(f"Error listing files in folder '{folder_path}': {e}\n")
        log_file.close()
        return

    for file in files:
        if file.lower().endswith('.pdf'):
            base_name = os.path.splitext(file)[0]
            if base_name in md_basenames:
                continue  # Skip if a matching .md file exists

            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                try:
                    kickof(file)
                    log_file.write(f"[SUCCESS] {file}\n")
                except Exception as e:
                    log_file.write(f"[FAILURE] {file} — {e}\n")

    log_file.close()
    print(f"\nLog saved to: {log_file_path}")

# Example usage
if __name__ == "__main__":
    folder = "./your-folder-path"       # Folder containing PDF files
    markdown_folder = "./markdown"      # Folder containing .md files
    process_pdf_files(folder, markdown_folder)
