from pathlib import Path
import os
from moviepy.editor import *


# Get url as argument
try:
    url = sys.argv[1]
    file = Path(url).stem

except:
    sys.exit("Usage: python3 thisfile.py URL")

video = VideoFileClip(url)
video.audio.write_audiofile("audio_output.mp3")
