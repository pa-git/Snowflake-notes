import os
import json

REQUIRED_JSON_FILES = [
    "acceptance_criteria.json",
    "business_context.json",
    "contract_metadata.json",
    "engagement_profile.json",
    "fee_breakdown.json",
    "file_name.json",
    "financials.json",
    "governance_methodology.json",
    "initiatives_projects.json",
    "milestones.json",
    "non_conforming_resources.json",
    "roles.json",
    "scope_delivery.json",
    "signatures.json",
    "slas.json",
    "tools_platforms.json",
    "travel_and_expense.json"
]

def merge_json_files_if_all_exist(subfolder_path):
    paths = [os.path.join(subfolder_path, fname) for fname in REQUIRED_JSON_FILES]

    if not all(os.path.isfile(p) for p in paths):
        print(f"Skipping {subfolder_path}: missing one or more required files.")
        return

    merged_data = {}
    for path, fname in zip(paths, REQUIRED_JSON_FILES):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                merged_data[fname.replace(".json", "")] = json.load(f)
            except json.JSONDecodeError:
                print(f"Invalid JSON in: {path}")
                return

    output_path = os.path.join(subfolder_path, "full_contract.json")
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(merged_data, out, indent=2)
    print(f"Created: {output_path}")


def process_all_subfolders(folder_path):
    for entry in os.scandir(folder_path):
        if entry.is_dir():
            merge_json_files_if_all_exist(entry.path)
