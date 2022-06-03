import youtube_dl
import sys


def youtube2mp3(youtube_video_url, save_as_file_name):
    """only for Youtube. The first argument is the Youtube video url
    the second argument is the file path and name for saving the mp3 file."""

    video_info = youtube_dl.YoutubeDL().extract_info(
        url=youtube_video_url, download=False
    )
    filename = f"{save_as_file_name}.mp3"
    options = {
        "format": "bestaudio/best",
        "keepvideo": False,
        "outtmpl": filename,
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info["webpage_url"]])
    print("Download complete... {}".format(filename))

    # for additional configuration options, visit the youtube_dl docs: https://github.com/ytdl-org/youtube-dl/blob/master/README.md#readme


if __name__ == "__main__":
    youtube_video_url = sys.argv[1]
    save_as_file_name = sys.argv[2]
    youtube2mp3(youtube_video_url, save_as_file_name)
