from TTS.api import TTS
from config import PATHS
from scipy.io.wavfile import write
import numpy as np
import re
import os
import json

# Audio parameters
SAMPLING_RATE = 22050  # default for Tacotron2
PAUSE_DURATION = 0.1   # seconds pause between sentences

def normalize_text(text: str) -> list[str]:
    """
    Clean and split text into short, safe sentences for TTS
    """
    # Remove unusual characters except basic punctuation
    text = re.sub(r"[^\w\s.,!?']", "", text)

    # Split into sentences using punctuation
    sentences = re.split(r"[.!?]", text)

    # Keep only non-empty, reasonably short sentences
    sentences = [s.strip() for s in sentences if 3 < len(s.strip()) < 120]

    return sentences

def generate_voice():
    """
    Generate TTS audio from script with chunking and pauses
    """
    tts = TTS(
        model_name="tts_models/en/ljspeech/tacotron2-DDC_ph",
        gpu=True  # use your local GPU
    )

    # LJSpeech has no speakers, use default
    speaker_name = None

    # Load script
    with open(PATHS["script"], "r") as f:
        text = f.read()

    sentences = normalize_text(text)

    if not sentences:
        raise ValueError("No valid sentences found in the script for TTS.")

    audio_chunks = []
    timings = []
    current_time = 0.0

    for sentence in sentences:
        # Generate waveform (numpy float32 array)
        wav = tts.tts(sentence, speaker=speaker_name, speed=2.0)
        duration = len(wav) / SAMPLING_RATE
        timings.append({'text': sentence, 'start': current_time, 'end': current_time + duration})
        current_time += duration + PAUSE_DURATION
        audio_chunks.append(wav)
        # Add small pause between sentences
        pause_samples = int(PAUSE_DURATION * SAMPLING_RATE)
        audio_chunks.append(np.zeros(pause_samples, dtype=np.float32))

    # Concatenate all chunks into one audio file
    final_audio = np.concatenate(audio_chunks)

    # Save as WAV
    os.makedirs(os.path.dirname(PATHS['audio']), exist_ok=True)
    write(PATHS["audio"], SAMPLING_RATE, final_audio)

    # Save timings
    timings_path = PATHS['audio'].replace('.wav', '_timings.json')
    with open(timings_path, 'w') as f:
        json.dump(timings, f)

    print(f"✓ Voice generated: {PATHS['audio']}")
