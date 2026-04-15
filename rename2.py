import os
import xml.etree.ElementTree as ET
import re
from config import FOLDER_INPUT

def ambil_nama_dari_xml(path_xml):
    tree = ET.parse(path_xml)
    root = tree.getroot()
    
    title = root.find(".//work-title")
    
    if title is None or not title.text:
        return os.path.splitext(os.path.basename(path_xml))[0]

    text = title.text.strip()

    match = re.match(r'^(\d+)\.\s*(.*)', text)
    if match:
        nomor = match.group(1)
        judul = match.group(2)
    else:
        nomor = ""
        judul = text

    judul = (
        judul.replace("Ŵ", "w")
             .replace("ŵ", "w")
             .replace("Ö", "o")
             .replace("ö", "o")
    )

    judul = judul.lower()
    judul = re.sub(r'\s+', '_', judul)
    judul = re.sub(r"[^a-z0-9_']", '', judul)

    if nomor:
        return f"{nomor}_{judul}"
    else:
        return judul


def rename_file_xml(path_xml):
    folder = os.path.dirname(path_xml)
    nama_baru = ambil_nama_dari_xml(path_xml) + ".xml"
    path_baru = os.path.join(folder, nama_baru)

    if path_xml == path_baru:
        print(f"SKIP: Nama sudah sesuai -> {nama_baru}")
        return

    if os.path.exists(path_baru):
        print(f"SKIP: File tujuan sudah ada -> {nama_baru}")
        return

    os.rename(path_xml, path_baru)
    print(f"RENAME: {os.path.basename(path_xml)} -> {nama_baru}")


if __name__ == "__main__":
    if not os.path.exists(FOLDER_INPUT):
        exit(f"Folder '{FOLDER_INPUT}' tidak ditemukan.")

    file_xmls = [f for f in os.listdir(FOLDER_INPUT) if f.endswith(".xml")]

    if not file_xmls:
        exit("Tidak ada file XML yang bisa diproses.")

    for f in file_xmls:
        path = os.path.join(FOLDER_INPUT, f)
        rename_file_xml(path)