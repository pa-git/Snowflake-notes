# List all .txt files in the directory
files = [f for f in os.listdir("your_directory") if f.endswith(".txt")]

# Sort numerically based on the number in the filename
sorted_files = sorted(files, key=lambda x: int(x.split('.')[0]))
