import os
import json

def convert_files_in_directory(directory_path, source_encoding, target_encoding):
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding=source_encoding) as file:
                    data = json.load(file)
                with open(f"{os.path.splitext(file_path)[0]}_converted.json", 'w', encoding=target_encoding) as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)


source_encoding = 'utf-16'
target_encoding = 'utf-8'
directory_path = './dist2'

convert_files_in_directory(directory_path, source_encoding, target_encoding)
