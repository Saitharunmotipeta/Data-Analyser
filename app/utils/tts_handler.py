import os
from gtts import gTTS

AUDIO_DIR = "static/audio"

def get_or_generate_tts(word: str) -> str:
    file_path = f"{AUDIO_DIR}/{word}.mp3"
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    if not os.path.exists(file_path):
        tts = gTTS(text=word, lang='en')
        tts.save(file_path)
    return file_path
