import subprocess
from unittest import result

from click import prompt
from config import NICHE_CONFIG, OLLAMA_MODEL




def run_llm(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL, prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()




def generate_idea():
    prompt = f"""
Generate 3 TikTok video ideas.
Niche: {NICHE_CONFIG['niche']}
Audience: {NICHE_CONFIG['audience']}
Tone: {NICHE_CONFIG['tone']}
Rules:
- Hook in first 2 seconds
- Faceless
- No emojis
Return plain text.
"""
    return run_llm(prompt)




def generate_script():
    prompt = f"""
Write ONLY spoken narration for a TikTok video.

Niche: {NICHE_CONFIG['niche']}
Tone: {NICHE_CONFIG['tone']}
Length: {NICHE_CONFIG['video_length_seconds']} seconds

Rules:
- Plain sentences only
- No emojis
- No brackets
- No labels (Narrator, Scene, etc.)
- Each sentence on a new line
- End with: {NICHE_CONFIG['cta']}
"""
    return run_llm(prompt)




def generate_caption():
    prompt = f"""
Write a short TikTok caption for this niche: {NICHE_CONFIG['niche']}.
Include exactly 3 hashtags.
No emojis.
"""
    return run_llm(prompt)