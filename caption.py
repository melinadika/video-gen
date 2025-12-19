import os

from config import PATHS
from llm import generate_caption




def save_caption():
    caption = generate_caption()
    os.makedirs(os.path.dirname(PATHS['caption']), exist_ok=True)
    with open(PATHS['caption'], "w", encoding="utf-8") as f:
        f.write(caption)