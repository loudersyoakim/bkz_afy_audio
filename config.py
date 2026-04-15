import os
import sys

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
BIN_FOLDER = os.path.join(BASE_PATH, "bin")
SF2_FOLDER = os.path.join(BIN_FOLDER, "sf2")

FOLDER_INPUT = os.path.join(BASE_PATH, "note_xml")
FOLDER_WAV = os.path.join(BASE_PATH, "music_output")
FOLDER_MP3 = os.path.join(BASE_PATH, "music_compressed")

FLUIDSYNTH_EXE = os.path.join(BIN_FOLDER, "fluidsynth.exe")
FFMPEG_EXE = os.path.join(BIN_FOLDER, "ffmpeg.exe")

# 4 SoundFont Final
SOUNDFONT_PIANO = os.path.join(SF2_FOLDER, "full_grand_piano.sf2")
SOUNDFONT_GLOCK = os.path.join(SF2_FOLDER, "glockenspiel.sf2")
SOUNDFONT_STRINGPAD = os.path.join(SF2_FOLDER, "198_sy1_Stringpad.sf2")
SOUNDFONT_DEEPS = os.path.join(SF2_FOLDER, "deep_strings.sf2")

def validate_dependencies():
    if not os.path.exists(FLUIDSYNTH_EXE): sys.exit("ERROR: fluidsynth.exe hilang!")
    if not os.path.exists(FFMPEG_EXE): sys.exit("ERROR: ffmpeg.exe hilang!")
    
    for sf in [SOUNDFONT_PIANO, SOUNDFONT_GLOCK, SOUNDFONT_STRINGPAD, SOUNDFONT_DEEPS]:
        if not os.path.exists(sf):
            sys.exit(f"CRITICAL ERROR: Soundfont '{os.path.basename(sf)}' tidak ditemukan!")