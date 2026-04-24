import os
import subprocess
from music21 import converter, note, chord
from config import (
    FLUIDSYNTH_EXE, FFMPEG_EXE, SOUNDFONT_PIANO, 
    SOUNDFONT_GLOCK, SOUNDFONT_STRINGPAD, SOUNDFONT_DEEPS
)
    
def humanize_velocity(stream):
    prev_pitch = None
    for n in stream.recurse():
        if isinstance(n, (note.Note, chord.Chord)):
            current_pitch = n.pitch.ps if isinstance(n, note.Note) else n.pitches[0].ps
            base_vel = 95 

            if current_pitch > 75: 
                reduction = (current_pitch - 75) * 1.5
                base_vel -= reduction

            if prev_pitch is not None:
                if abs(current_pitch - prev_pitch) > 12:
                    base_vel *= 0.8  

            n.volume.velocity = max(30, min(127, int(base_vel)))
            prev_pitch = current_pitch

def xml_to_midi(file_xml, file_midi):
    print(f"1. Membaca & Humanisasi XML: {os.path.basename(file_xml)}...")
    partitur = converter.parse(file_xml)
    humanize_velocity(partitur)
    partitur.write('midi', fp=file_midi)

def _render_fluid(file_midi, file_wav, sf2_path, gain_vol="1.0"):
    cmd_fluid = [
        FLUIDSYNTH_EXE, "-ni", "-g", gain_vol,
        "-o", "synth.reverb.active=yes",
        "-o", "synth.reverb.room-size=0.9",
        "-o", "synth.reverb.level=0.5",
        "-o", "synth.chorus.active=yes",
        "-T", "wav", "-F", file_wav, sf2_path, file_midi
    ]
    subprocess.run(cmd_fluid, capture_output=True, text=True)

def render_layers_to_wav(file_midi, wav_piano, wav_glock, wav_pad, wav_deeps):
    print("2. Rendering Piano...")
    _render_fluid(file_midi, wav_piano, SOUNDFONT_PIANO, gain_vol="2.5")
    
    print("3. Rendering Glockenspiel...")
    _render_fluid(file_midi, wav_glock, SOUNDFONT_GLOCK, gain_vol="0.35")

    print("4. Rendering Stringpad...")
    _render_fluid(file_midi, wav_pad, SOUNDFONT_STRINGPAD, gain_vol="0.4")

    print("5. Rendering Deep Strings...")
    _render_fluid(file_midi, wav_deeps, SOUNDFONT_DEEPS, gain_vol="1.5")

def mix_and_compress(wav_piano, wav_glock, wav_pad, wav_deeps, file_mp3):
    print("6. Mixing 4 Audio Layers...")
    cmd_ffmpeg = [
        FFMPEG_EXE, "-y", "-i", wav_piano, "-i", wav_glock, "-i", wav_pad, "-i", wav_deeps,
        "-filter_complex", "amix=inputs=4:duration=longest,areverse,silenceremove=start_periods=1:start_duration=0.5:start_threshold=-50dB,areverse",
        "-codec:a", "libmp3lame", "-q:a", "4", "-ar", "44100", file_mp3
    ]
    subprocess.run(cmd_ffmpeg, capture_output=True, text=True)
    return os.path.getsize(file_mp3) / 1024