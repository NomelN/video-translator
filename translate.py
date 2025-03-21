import os
import subprocess
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS



# Dossier de stockage des fichiers
UPLOAD_FOLDER = 'static/uploads'
TRANSLATE_FOLDER = 'static/translate'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSLATE_FOLDER, exist_ok=True)


def extract_audio(video_path, audio_path):
    command = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-q:a', '0',
        '-map', 'a',
        audio_path
    ]
    subprocess.run(command, check=True)


def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="en")
    return result.get("text", "")

def translate_text(text, source='en', target='fr'):
    translator = GoogleTranslator(source=source, target=target)
    return translator.translate(text)


def text_to_speech(text, tts_path):
    tts = gTTS(text=text, lang='fr')
    tts.save(tts_path)

def replace_audio_in_video(video_path, audio_path, output_path):
    command = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        output_path
    ]
    subprocess.run(command, check=True)

def process_video(video_filename):
    video_path = os.path.join(UPLOAD_FOLDER, video_filename)
    base_filename = os.path.splitext(video_filename)[0]
    audio_path = f'{base_filename}_audio.wav'
    tts_path = f'{base_filename}_tts.mp3'
    output_filename = f"{base_filename}_translated.mp4"
    output_path = os.path.join(TRANSLATE_FOLDER, output_filename)

    print("Extraction de l'audio...")
    extract_audio(video_path, audio_path)
    print("Audio extrait:", audio_path)

    text_en = transcribe_audio(audio_path)
    print("Transcription terminée")
    
    # Sauvegarder le texte transcrit dans un fichier .txt
    transcript_filename = f"{base_filename}_transcript_en.txt"
    transcript_path = os.path.join(TRANSLATE_FOLDER, transcript_filename)
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(text_en) # type: ignore

    text_fr = translate_text(text_en)
    print("Traduction terminée")

    # Sauvegarder le texte traduit dans un fichier .txt
    transcript_filename_fr = f"{base_filename}_transcript_fr.txt"
    transcript_path_fr = os.path.join(TRANSLATE_FOLDER, transcript_filename_fr)
    with open(transcript_path_fr, 'w', encoding='utf-8') as f:
        f.write(text_fr)
    print("Texte traduit sauvegardé:", transcript_path_fr)

    text_to_speech(text_fr, tts_path)
    print("Synthèse vocale terminée:", tts_path)

    replace_audio_in_video(video_path, tts_path, output_path)
    print("Vidéo traduite générée:", output_path)

    # Vous pouvez également vérifier que le fichier existe :
    if os.path.exists(output_path):
        print("Le fichier de sortie existe.")
    else:
        print("Le fichier de sortie n'existe pas.")
    
    # Optionnel : nettoyage des fichiers temporaires
    os.remove(audio_path)
    os.remove(tts_path)

    return output_filename