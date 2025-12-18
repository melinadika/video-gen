from config import PATHS
from llm import generate_caption




def save_caption():
    caption = generate_caption()
    with open(PATHS['caption'], "w") as f:
        f.write(caption)