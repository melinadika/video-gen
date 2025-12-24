"""
FREE TikTok AI Pipeline (Single Account)


Requirements:
- Python 3.11
- FFmpeg
- Ollama (with mistral model)


Install:
- pip install openai-whisper TTS
- pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
- pip install diffusers==0.27.2


Usage:
1. Edit config.py (niche, tone, CTA)
2. Add a looping background video to data/visuals/bg.mp4
3. Run: python run.py
4. Upload final video manually to TikTok


This repo is intentionally simple and safe for early experimentation.
"""