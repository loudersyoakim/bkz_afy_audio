import os
from datetime import datetime

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
folder_path = os.path.join(BASE_PATH, "note_angka")
start_number = 8

files = [f for f in os.listdir(folder_path) if f.startswith("Screenshot")]

def extract_datetime(name):
    parts = name.replace("Screenshot ", "").split(".")[0]
    return datetime.strptime(parts, "%Y-%m-%d %H%M%S")

files.sort(key=extract_datetime)

for i, filename in enumerate(files, start=start_number):
    old_path = os.path.join(folder_path, filename)
    ext = os.path.splitext(filename)[1]
    new_name = f"{i}{ext}"
    new_path = os.path.join(folder_path, new_name)

    os.rename(old_path, new_path)
    print(f"{filename} -> {new_name}")

print("Selesai!")