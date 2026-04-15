import os
import time
import xml.etree.ElementTree as ET
import re
from config import BASE_PATH, FOLDER_INPUT, FOLDER_WAV, FOLDER_MP3, validate_dependencies
import converter

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
        return f"{nomor}"
    else:
        return judul
    
def proses_single_file(path_xml):
    print(f"Sedang memproses file: {path_xml}")
    nama_dasar = ambil_nama_dari_xml(path_xml)    
    # Siapkan 4 slot WAV
    wav_piano = os.path.join(FOLDER_WAV, f"{nama_dasar}_piano.wav")
    wav_glock = os.path.join(FOLDER_WAV, f"{nama_dasar}_glock.wav")
    wav_pad = os.path.join(FOLDER_WAV, f"{nama_dasar}_pad.wav")
    wav_deeps = os.path.join(FOLDER_WAV, f"{nama_dasar}_deeps.wav")
    
    path_mp3 = os.path.join(FOLDER_MP3, f"{nama_dasar}.mp3")
    file_midi = os.path.join(BASE_PATH, f"temp_{nama_dasar}.mid")

    if os.path.exists(path_mp3):
        print(f"SKIP: {nama_dasar} sudah selesai dikompresi.")
        return

    os.makedirs(FOLDER_WAV, exist_ok=True)
    os.makedirs(FOLDER_MP3, exist_ok=True)

    try:
        converter.xml_to_midi(path_xml, file_midi)
        
        # Render 4 layer
        converter.render_layers_to_wav(file_midi, wav_piano, wav_glock, wav_pad, wav_deeps)
        time.sleep(1)
        
        # Mix 4 file jadi 1 MP3
        ukuran_mp3 = converter.mix_and_compress(wav_piano, wav_glock, wav_pad, wav_deeps, path_mp3)
        time.sleep(0.5)

        print(f"BERHASIL! {os.path.basename(path_mp3)} tercipta ({ukuran_mp3:.0f} KB).\n")

    except Exception as e:
        print(f"ERROR memproses {nama_dasar}: {e}\n")
    finally:
        # Bersihkan 5 file sementara
        for temp_file in [file_midi, wav_piano, wav_glock, wav_pad, wav_deeps]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

if __name__ == "__main__":
    validate_dependencies()
    
    if not os.path.exists(FOLDER_INPUT):
        exit(f"Folder '{FOLDER_INPUT}' tidak ditemukan.")

    file_xmls = [f for f in os.listdir(FOLDER_INPUT) if f.endswith(".xml")]
    if not file_xmls:
        exit("Tidak ada file XML yang bisa diproses.")
    
    for f in file_xmls:
        proses_single_file(os.path.join(FOLDER_INPUT, f))