def has_file(subfolder_name, base_folder, file_name):
    """
    Given a subfolder name, base folder, and file name,
    return True if the file exists in that subfolder, else False.
    """
    full_path = os.path.join(base_folder, subfolder_name, file_name)
    return os.path.isfile(full_path)
