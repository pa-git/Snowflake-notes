def has_full_contract_json(subfolder_name, base_folder):
    """
    Given a subfolder name and base folder path,
    return True if full_contract.json exists in that subfolder, else False.
    """
    full_path = os.path.join(base_folder, subfolder_name)
    target_file = os.path.join(full_path, "full_contract.json")
    return os.path.isfile(target_file)
