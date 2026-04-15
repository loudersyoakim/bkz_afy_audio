# Note2Music: XML to MP3 Batch Converter

Proyek automasi Python untuk mengonversi partitur musik digital (MusicXML) menjadi file audio MP3 berkualitas tinggi secara massal (_batch processing_).

Script ini menggunakan **music21** untuk membaca XML, **FluidSynth** untuk merender instrumen nyata menggunakan SoundFont (.sf2), dan **FFmpeg** untuk mengompresi audio serta memotong keheningan (_silence removal_) secara otomatis.

## Fitur Utama

- **Batch Processing:** Memproses puluhan/ratusan file XML dalam satu folder sekaligus.
- **Auto-Skip:** Melewati file yang sudah pernah dirender, sangat hemat waktu.
- **High-Quality Audio:** Menggunakan VBR (Variable Bitrate) MP3 dan efek Reverb/Chorus agar suara instrumen (Piano) terdengar "hidup" dan natural.
- **Smart Silence Removal:** Otomatis memotong keheningan/suara kosong di akhir lagu secara presisi.
- **Auto-Cleanup:** Otomatis membersihkan file MIDI sementara dan file WAV raksasa setelah kompresi MP3 selesai.

---

## Persiapan & Prasyarat (Wajib Dibaca)

Karena batasan ukuran file dan hak cipta, program pendukung (_executable_) dan SoundFont **TIDAK** disertakan di dalam repositori ini. Anda harus mengunduh dan menyiapkannya secara manual.

### 1. Instalasi Library Python

Pastikan Anda sudah menginstal Python 3.x. Buka terminal dan jalankan:
`pip install music21`

### 2. Download FluidSynth (Render Audio)

1. Pergi ke halaman rilis [FluidSynth GitHub](https://github.com/FluidSynth/fluidsynth/releases).
2. Download versi Windows (Cari file zip berakhiran `win10-x64-glib.zip`).
3. Ekstrak file zip, buka folder `bin`.
4. Copy `fluidsynth.exe` beserta **semua file `.dll`** ke dalam folder utama proyek ini.

### 3. Download FFmpeg (Kompresi Audio)

1. Pergi ke halaman [FFmpeg Master Builds](https://github.com/BtbN/FFmpeg-Builds/releases).
2. Download file `ffmpeg-master-latest-win64-gpl.zip`.
3. Ekstrak file zip, buka folder `bin`.
4. Copy `ffmpeg.exe` ke dalam folder utama proyek ini.

### 4. Siapkan SoundFont (.sf2)

Anda memerlukan file rekaman instrumen asli (SoundFont).

1. Download SoundFont Piano gratis seperti **Salamander Grand Piano** atau **FluidR3_GM**.
2. Ubah nama file menjadi `full_grand_piano.sf2` (atau sesuaikan variabel `SOUNDFONT` di dalam kode Python).
3. Letakkan file tersebut di dalam folder utama proyek.
