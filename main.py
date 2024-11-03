import pytubefix
from pytubefix.cli import on_progress
import os
import whisper

def download_audio(url, output_folder = "audio_files"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    yt = pytubefix.YouTube(url, on_progress_callback = on_progress)
    print(yt.title)

    ys = yt.streams.get_audio_only()
    audio_path = ys.download(output_path=output_folder)

    return audio_path

def transcription_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result['text']


url = input("Coloque a url: ")
audio_path = download_audio(url)

transcription = transcription_audio(audio_path)
print(transcription)