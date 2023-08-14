import os

def get_matching_txt_files(folder_path, prefix):
    matching_files = []
    for filename in os.listdir(folder_path):
        if filename.startswith(prefix) and filename.endswith(".txt"):
            matching_files.append(filename)
    return matching_files

folder_path = "./"  # Substitua pelo caminho da sua pasta
prefix = "rolling_data"

txt_files = get_matching_txt_files(folder_path, prefix)
for txt_file in txt_files:
    print(txt_file)