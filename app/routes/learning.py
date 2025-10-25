from fastapi import APIRouter, Form
from app.utils.phonetics import get_phonetics_syllables
from app.utils.tts_handler import get_or_generate_tts

router = APIRouter(prefix="/learn", tags=["Learning"])

@router.post("/process")
async def process_word(word: str = Form(...)):
    data = get_phonetics_syllables(word)
    audio_path = get_or_generate_tts(word)
    return {
        "word": word,
        "syllables": data["syllables"],
        "phonemes": data["phonemes"],
        "audio_url": f"/{audio_path}"
    }
