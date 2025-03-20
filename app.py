import os
import uuid
import subprocess
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS

app = Flask(__name__)
app.secret_key = 'secret'


# Dossier de stockage des fichiers
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/translate'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


def extract_audio(video_path, audio_path):
    command = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-q:a', '0',
        '-map', 'a',
        audio_path
    ]
    subprocess.run(command, check=True)





if __name__ == '__main__':
    app.run(debug=True)