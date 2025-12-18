import whisper
from config import PATHS

def seconds_to_srt_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def generate_subtitles():
    model = whisper.load_model("base")
    result = model.transcribe(
        PATHS["audio"],
        language="en",
        task="transcribe",
        word_timestamps=True
    )
    with open(PATHS['subs'], "w") as f:
        for i, seg in enumerate(result["segments"]):
            start = seconds_to_srt_time(seg["start"])
            end = seconds_to_srt_time(seg["end"])

            f.write(f"{i+1}\n")
            f.write(f"{start} --> {end}\n")
            f.write(seg["text"].strip() + "\n\n")
