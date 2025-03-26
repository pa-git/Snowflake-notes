import os

directory = '/path/to/directory'

# List all files and directories
files = os.listdir(directory)

# Filter and list only files
file_list = [f for f in files if os.path.isfile(os.path.join(directory, f))]
