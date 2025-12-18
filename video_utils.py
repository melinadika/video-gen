import subprocess
import os
from config import PATHS

def assemble_video():
    subs_path = os.path.abspath(PATHS['subs'])
    bg_path = os.path.abspath(PATHS['bg'])
    audio_path = os.path.abspath(PATHS['audio'])
    out_path = os.path.abspath(PATHS['video'])

    cmd = [
        "ffmpeg",
        "-y",
        "-i", bg_path,
        "-i", audio_path,
        "-vf", f"subtitles='{subs_path}'",
        "-map", "0:v",
        "-map", "1:a",
        "-shortest",
        out_path
    ]

    subprocess.run(cmd, check=True)