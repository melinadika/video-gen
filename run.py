import argparse
from llm import generate_idea, generate_script
from tts import generate_voice
from subtitles import generate_subtitles
from video_utils import assemble_video
from caption import save_caption
from config import PATHS




def main(args):
    if args.idea:
        idea = generate_idea()
        open(PATHS['ideas'], "w").write(idea)
        print("Generated Ideas")
    if args.script:
        script = generate_script()
        open(PATHS['script'], "w").write(script)
        print("Generated Script")
    if args.tts:
        generate_voice()
        print("Generated Voice")
    if args.subs:
        generate_subtitles()
        print("Generated Subtitles")
    if args.video:
        assemble_video()
        print("Assembled Video")
    if args.caption:
        save_caption()
        print("Saved Caption")

    print("DONE")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--idea", action="store_true", help="Generate idea")
    parser.add_argument("--script", action="store_true", help="Generate script")
    parser.add_argument("--tts", action="store_true", help="Generate voice")
    parser.add_argument("--subs", action="store_true", help="Generate subtitles")
    parser.add_argument("--video", action="store_true", help="Assemble video")
    parser.add_argument("--caption", action="store_true", help="Save caption")

    args = parser.parse_args()

    # Default behavior: run everything if no flags provided
    if not any(vars(args).values()):
        args.idea = True
        args.script = True
        args.tts = True
        args.subs = True
        args.video = True
        args.caption = True

    main(args)