import pytubefix
from pytubefix.cli import on_progress
import os
import whisper
from transformers import pipeline


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

def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    chunk_size = 1024 
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    
    final_summary = ' '.join(summaries)
    return final_summary

url = input("Coloque a url: ")
audio_path = download_audio(url)

try:
    transcription = transcription_audio(audio_path)
    summary = summarize_text(transcription)
    print(summary)
finally:
    if os.path.exists(audio_path):
        os.remove(audio_path)