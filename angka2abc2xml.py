import os
import re
import time
import google.generativeai as genai
from pathlib import Path
from PIL import Image, ImageOps
from google.api_core import exceptions

# Tambahan Library untuk Konversi Lokal
try:
    from music21 import converter, environment
except ImportError:
    print("❌ Library music21 belum terinstall. Jalankan: pip install music21")
    exit()

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = "AIzaSyAj4lCCB-Osx6OQJt0ZCfFy3uifVIMQy0k" # Ingat, amankan API key kamu!
INPUT_FOLDER  = Path("note_angka")
ABC_FOLDER    = Path("temp_abc")       # Folder sementara untuk ABC
OUTPUT_FOLDER = Path("note_xml_beta")  # Hasil akhir XML
MODEL_NAME = "gemini-2.5-flash"        # Wajib 1.5 Flash agar stabil & tidak error 404

genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,           
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=generation_config
)

# ==========================================
# PROMPT SAKRAL (ANTI-NGEYEL ANGKA)
# ==========================================
PROMPT_SISTEM = (
    "Kamu adalah transkriber profesional Not Angka ke ABC Notation standar.\n"
    "TUGAS MUTLAK: TERJEMAHKAN SETIAP ANGKA MENJADI HURUF NADA. JANGAN PERNAH MENCETAK ANGKA UNTUK MELODI!\n\n"
    "ATURAN TRANSLASI:\n"
    "- Nada dasar: 1=C, 2=D, 3=E, 4=F, 5=G, 6=A, 7=B, 0=z (istirahat).\n"
    "- Durasi: '1 .' jadi C2 | '1 . .' jadi C3.\n"
    "- Durasi (Garis bawah): jadikan /2 (contoh: C/2 D/2).\n"
    "- Oktaf: Titik di ATAS = huruf kecil (c). Titik di BAWAH = huruf besar tambah koma (C,).\n\n"
    "CONTOH KASUS:\n"
    "Gambar terlihat: 1 5 1 | 3 . 2 | 1 3 3 | 4 | 5 5 . |]\n"
    "Output ABC BENAR: C G C | E2 D | C E E | F | G G2 |]\n\n"
    "ATURAN FORMAT ABC:\n"
    "1. Mulai dari X:1\n"
    "2. Wajib ada T: (Judul Lagu yang tertulis di gambar)\n"
    "3. Pastikan header K:C\n"
    "4. JANGAN output baris lirik (w:). JANGAN gunakan V:. HANYA melodi murni tanpa markdown."
)

def clean_abc(text: str) -> str:
    """Bersihkan markdown dan lirik"""
    text = re.sub(r'```[a-z]*|```', '', text).strip()
    idx = text.find('X:')
    if idx != -1:
        text = text[idx:]

    lines = text.splitlines()
    clean_lines = [
        line for line in lines 
        if not line.strip().startswith("w:") and not line.strip().startswith("V:")
    ]
    return "\n".join(clean_lines).strip()

def get_safe_filename(abc_text: str, fallback_name: str) -> str:
    """Ekstrak judul dari tag T: dan jadikan nama file yang bersih"""
    match = re.search(r'^T:\s*(.*)', abc_text, re.MULTILINE)
    if match:
        raw_title = match.group(1).strip().lower()
        # Ubah semua karakter selain huruf dan angka menjadi underscore (_)
        safe_title = re.sub(r'[^a-z0-9]+', '_', raw_title)
        # Hapus underscore berlebih di ujung
        safe_title = safe_title.strip('_')
        if safe_title:
            return safe_title
    return fallback_name

def compress_image(img_path) -> Image.Image:
    """Grayscale + resize agar hemat TPM."""
    img = Image.open(img_path)
    img = ImageOps.grayscale(img)
    base_width = 1000
    ratio = base_width / float(img.size[0])
    h = int(img.size[1] * ratio)
    img = img.resize((base_width, h), Image.Resampling.LANCZOS)
    tmp = "temp_optimized.jpg"
    img.save(tmp, "JPEG", quality=70)
    return Image.open(tmp)

def convert_abc_to_xml_local(abc_path, xml_path):
    """Fungsi lokal merubah .abc jadi .xml"""
    try:
        score = converter.parse(abc_path)
        score.write('musicxml', fp=xml_path)
        return True
    except Exception as e:
        print(f"\n   ⚠️ Gagal parsing ABC: {e}")
        return False

def run_pipeline():
    INPUT_FOLDER.mkdir(exist_ok=True)
    ABC_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)

    all_files = sorted(
        list(INPUT_FOLDER.glob("*.png")) +
        list(INPUT_FOLDER.glob("*.jpg")) +
        list(INPUT_FOLDER.glob("*.jpeg"))
    )
    total = len(all_files)

    if total == 0:
        print(f"❌ Folder '{INPUT_FOLDER}' kosong!")
        return

    print(f"🚀 Memulai Pipeline Auto-Rename: {total} file\n")

    i = 0
    while i < total:
        img_path  = all_files[i]
        abc_path  = ABC_FOLDER / f"{img_path.stem}.abc"

        # --- LOGIKA SMART RESUME ---
        if abc_path.exists():
            with open(abc_path, "r", encoding="utf-8") as f:
                existing_abc = f.read()
            
            # Cek nama XML berdasarkan ABC yang sudah ada
            safe_name = get_safe_filename(existing_abc, img_path.stem)
            xml_path  = OUTPUT_FOLDER / f"{safe_name}.xml"

            if xml_path.exists():
                print(f"[{i+1}/{total}] ⏩ Skip: {img_path.name} (Sudah jadi: {xml_path.name})")
                i += 1
                continue
            else:
                # ABC ada tapi XML belum jadi? Konversi sekarang tanpa panggil AI!
                print(f"[{i+1}/{total}] ⚡ Resume Lokal: {abc_path.name} -> {xml_path.name}...", end=" ")
                success = convert_abc_to_xml_local(abc_path, xml_path)
                if success: print("✅ TUNTAS")
                i += 1
                continue

        # --- JIKA BELUM ADA ABC, PANGGIL AI ---
        try:
            print(f"[{i+1}/{total}] 🔄 Memproses AI: {img_path.name}...", end=" ", flush=True)
            img_opt = compress_image(img_path)

            chat = model.start_chat()
            response = chat.send_message([PROMPT_SISTEM, img_opt])

            if not response.text:
                print("❌ GAGAL (Respons Kosong)")
                i += 1
                continue

            raw_text = response.text

            max_cont  = 2
            cont_count = 0
            while response.candidates and response.candidates[0].finish_reason.value == 2:
                if cont_count >= max_cont:
                    print("\n   [!] Terlalu panjang, stop.", end=" ")
                    break
                print("\n   [!] Terpotong, lanjut...", end=" ", flush=True)
                time.sleep(3)
                response = chat.send_message("Lanjutkan ABC notation persis dari karakter terakhir.")
                raw_text  += response.text
                cont_count += 1

            abc_data = clean_abc(raw_text)

            # Simpan ABC sebagai rekam jejak
            with open(abc_path, "w", encoding="utf-8") as f:
                f.write(abc_data)
                
            # EKSTRAK NAMA FILE DARI JUDUL
            safe_name = get_safe_filename(abc_data, img_path.stem)
            xml_path  = OUTPUT_FOLDER / f"{safe_name}.xml"
            
            print(f" | Menyimpan sbg: {xml_path.name}...", end=" ")
            success = convert_abc_to_xml_local(abc_path, xml_path)
            
            if success:
                print("✅ TUNTAS")
            
            i += 1
            time.sleep(12)

        except exceptions.ResourceExhausted:
            print("\n🛑 LIMIT TERCAPAI! Menunggu 60 detik...")
            time.sleep(60)

        except Exception as e:
            print(f"\n❌ Error pada {img_path.name}: {e}")
            i += 1
            time.sleep(5)

    if os.path.exists("temp_optimized.jpg"):
        os.remove("temp_optimized.jpg")

    print(f"\n🎉 Selesai! Semua XML sudah dinamai dengan cantik di folder: {OUTPUT_FOLDER}")

if __name__ == "__main__":
    run_pipeline()