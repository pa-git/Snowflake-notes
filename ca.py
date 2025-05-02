import json

# Replace with your actual file path
file_path = "path/to/your/file.json"

# Load the JSON file
with open(file_path, "r") as f:
    data = json.load(f)

# Retrieve the vendor_name
vendor_name = data.get("contract_metadata", {}).get("vendor_name")

print("Vendor Name:", vendor_name)
