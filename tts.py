from TTS.api import TTS
from config import PATHS
from scipy.io.wavfile import write
import numpy as np
import re
import os
import json

# XTTS audio params
SAMPLING_RATE = 24000
PAUSE_DURATION = 0.1

VOICE_WAV = "data/voice/narrator.wav"

def normalize_text(text: str) -> list[str]:
    text = re.sub(r"[^\w\s.,!?']", "", text)
    sentences = re.split(r"[.!?]", text)
    return [s.strip() for s in sentences if 3 < len(s.strip()) < 120]

def normalize_audio(wav: np.ndarray) -> np.ndarray:
    """Normalize audio to [-1, 1] safely"""
    max_val = np.max(np.abs(wav))
    if max_val > 0:
        wav = wav / max_val
    return np.clip(wav, -1.0, 1.0)

def generate_voice():
    tts = TTS(
        model_name="tts_models/multilingual/multi-dataset/xtts_v2"
    ).to("cuda")

    with open(PATHS["script"], "r") as f:
        text = f.read().strip()

    sentences = normalize_text(text)
    if not sentences:
        raise ValueError("No valid sentences for TTS")

    audio_chunks = []
    timings = []
    current_time = 0.0

    for sentence in sentences:
        wav = tts.tts(
            text=sentence,
            speaker_wav=VOICE_WAV,
            language="en",
        )

        wav = np.asarray(wav, dtype=np.float32)
        wav = normalize_audio(wav)

        duration = len(wav) / SAMPLING_RATE

        timings.append({
            "text": sentence,
            "start": round(current_time, 3),
            "end": round(current_time + duration, 3)
        })

        audio_chunks.append(wav)
        current_time += duration

        pause = np.zeros(int(PAUSE_DURATION * SAMPLING_RATE), dtype=np.float32)
        audio_chunks.append(pause)
        current_time += PAUSE_DURATION

    final_audio = np.concatenate(audio_chunks)
    final_audio = normalize_audio(final_audio)

    os.makedirs(os.path.dirname(PATHS["audio"]), exist_ok=True)
    write(PATHS["audio"], SAMPLING_RATE, final_audio)

    with open(PATHS["audio"].replace(".wav", "_timings.json"), "w") as f:
        json.dump(timings, f, indent=2)

    print(f"✓ XTTS voice generated: {PATHS['audio']}")
