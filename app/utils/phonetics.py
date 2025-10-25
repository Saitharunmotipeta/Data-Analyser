import os
from phonemizer import phonemize
import pyphen

# Point to the new location
os.environ['PHONEMIZER_ESPEAK_PATH'] = r"C:\Users\saitharun\eSpeak NG\espeak-ng.exe"

def get_phonetics_syllables(word: str):
    # Syllables using pyphen
    dic = pyphen.Pyphen(lang='en')
    syllables = dic.inserted(word).split('-')

    # Phonemes using Phonemizer
    phonemes = phonemize(
        word,
        language='en-us',
        backend='espeak',  # use 'espeak' backend, not 'espeak-ng'
        strip=True,
        preserve_punctuation=True
    ).split()

    return {"syllables": syllables, "phonemes": phonemes}

# Test
print(get_phonetics_syllables("hello"))
