from pathlib import Path

file_path = Path("output/json/full_contract.json")

if file_path.exists():
    with file_path.open("r", encoding="utf-8") as f:
        content = f.read()
        print("📄 File content loaded:")
        print(content)
else:
    print("❌ File does not exist.")
