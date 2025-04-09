import os
from datetime import datetime

# Dummy kickof function for illustration
def kickof(filename):
    # Replace this with your actual logic
    if "fail" in filename.lower():
        raise ValueError("Simulated failure")
    print(f"Processing {filename}")

def process_pdf_files(folder_path):
    # Prepare logs folder and file
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = f"logs/process_log_{timestamp}.txt"

    try:
        log_file = open(log_file_path, "w", encoding="utf-8")
    except Exception as e:
        print(f"Unable to open log file: {e}")
        return

    try:
        files = os.listdir(folder_path)
    except Exception as e:
        log_file.write(f"Error listing files in folder '{folder_path}': {e}\n")
        log_file.close()
        return

    for file in files:
        if file.lower().endswith('.pdf'):
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
    folder = "./your-folder-path"  # change this to your actual path
    process_pdf_files(folder)
