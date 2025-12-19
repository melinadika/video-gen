import json
import os
from config import PATHS

def seconds_to_srt_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def generate_subtitles():
    # Load timings from TTS
    timings_path = PATHS['audio'].replace('.wav', '_timings.json')
    with open(timings_path, 'r') as f:
        timings = json.load(f)
    
    os.makedirs(os.path.dirname(PATHS['subs']), exist_ok=True)
    with open(PATHS['subs'], "w", encoding='utf-8') as f:
        for i, timing in enumerate(timings):
            start = timing['start']
            end = timing['end']
            text = timing['text']
            start_time = seconds_to_srt_time(start)
            end_time = seconds_to_srt_time(end)
            
            f.write(f"{i+1}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(text + "\n\n")
