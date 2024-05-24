import os

# List of allowed file extensions
allowed_extensions = ['.js', '.py', '.json', '.html', '.css', '.yml', 'Dockerfile', '.sh', '.wxml', '.wxss']

def write_file_content(file_path, output_file):
    relative_path = os.path.relpath(file_path)
    output_file.write(f"\n\n=== Filename: {file_path} Start ===\n\n")
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                output_file.write(line)
    output_file.write(f"\n\n=== Filename: {file_path} End ===\n\n")

def find_and_write_files(base_directory, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for root, _, files in os.walk(base_directory):
            for file in files:
                if any(file.endswith(ext) for ext in allowed_extensions):
                    full_file_path = os.path.join(root, file)
                    if os.path.isfile(full_file_path):
                        write_file_content(full_file_path, output_file)
                    else:
                        output_file.write(f"File not found: {full_file_path}\n\n")

# Base directory containing all the files
base_directory = './django'

# Replace this with your desired output file path
output_filename = './django.src.txt'

# Call the function to write the specified files' contents
find_and_write_files(base_directory, output_filename)
