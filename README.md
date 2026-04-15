# Note2Music: XML to MP3 Batch Converter (BKZ AFY Edition)

Proyek automasi Python untuk mengonversi partitur musik digital (MusicXML) menjadi file audio MP3 berkualitas tinggi secara massal (_batch processing_), khusus dikembangkan untuk kebutuhan **BKZ AFY**.

Script ini menggunakan **music21** untuk membaca XML, **FluidSynth** untuk merender instrumen menggunakan berbagai SoundFont (.sf2) berkualitas tinggi, dan **FFmpeg** untuk kompresi audio serta pemotongan keheningan (_silence removal_).

## Fitur Utama

- **BKZ AFY Optimized:** Konfigurasi khusus untuk proyek Buku Zinuno dengan karakter suara yang lebih kaya.
- **Multi-SoundFont Support:** Mendukung penggunaan Strings Pad dan Glockenspiel untuk hasil audio yang lebih megah.
- **Batch Processing:** Memproses puluhan/ratusan file XML dalam satu folder sekaligus.
- **Smart Silence Removal:** Otomatis memotong keheningan di akhir lagu secara presisi.
- **Auto-Cleanup:** Otomatis menghapus file MIDI dan WAV sementara setelah MP3 selesai dibuat.

---

## Persiapan & Prasyarat (Wajib Dibaca)

Karena batasan ukuran file, program pendukung (_executable_) dan SoundFont **TIDAK** disertakan di repositori ini. Anda harus menyiapkannya secara manual.

### 1. Instalasi Library Python
`pip install music21`

### 2. Download FluidSynth (Renderer)
1. Download versi Windows dari [FluidSynth GitHub](https://github.com/FluidSynth/fluidsynth/releases) (cari `win10-x64-glib.zip`).
2. Ekstrak dan copy `fluidsynth.exe` serta **semua file .dll** ke folder utama proyek.

### 3. Download FFmpeg (Compressor)
1. Download dari [FFmpeg Master Builds](https://github.com/BtbN/FFmpeg-Builds/releases).
2. Copy `ffmpeg.exe` ke folder utama proyek.

### 4. Setup SoundFont (.sf2) — Khusus BKZ AFY
Untuk mendapatkan karakter suara yang sesuai, unduh dan siapkan SoundFont berikut:


| Instrumen | Sumber Download | Nama File di Proyek |
| :--- | :--- | :--- |
| **Piano Utama** | [Grand Piano](https://github.com/draconian9908/RadialSynth/blob/master/sound_files/Full%20Grand%20Piano.sf2) | `full_grand_piano.sf2` |
| **Strings Pad 1** | [198 SY1 Stringpad](https://www.zanderjaz.com/soundfonts/strings/198_sy1_Stringpad.sf2) | `stringpad_1.sf2` |
| **Deep Strings** | [Deep Strings SF2](https://www.zanderjaz.com/soundfonts/strings/Deep%20Strings.SF2) | `deep_strings.sf2` |
| **Glockenspiel** | [Ethan Winer Glockenspiel](https://ethanwiner.com/glockenspiel.zip) | `glockenspiel.sf2` |

> **Catatan:** Untuk Glockenspiel, ekstrak file `.zip` terlebih dahulu dan ambil file `.sf2`-nya saja. Letakkan semua file di atas di folder utama proyek atau folder `assets/soundfonts/`.

---

## Cara Penggunaan
1. Letakkan file `.xml` Anda di folder input.
2. Pastikan semua file `.exe` dan `.sf2` sudah berada di tempatnya.
3. Jalankan script:
   ```bash
   python main.py
