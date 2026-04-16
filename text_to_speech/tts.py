import os
import io
import wave
from piper.voice import PiperVoice

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Relative path to the model downloaded via huggingface_hub
MODEL_PATH = os.path.join(CURRENT_DIR, "models", "en", "en_US", "lessac", "medium", "en_US-lessac-medium.onnx")

# Load model globally to avoid reloading overhead
_voice = None

def get_voice():
    global _voice
    if _voice is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Piper TTS model not found at {MODEL_PATH}. Please ensure it is downloaded.")
        _voice = PiperVoice.load(MODEL_PATH)
    return _voice

def generate_speech(text: str) -> bytes:
    """
    Generates speech audio bytes in WAV format from the given text using Piper TTS.
    """
    voice = get_voice()
    audio_stream = io.BytesIO()
    
    with wave.open(audio_stream, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes for 16-bit
        wav_file.setframerate(voice.config.sample_rate)
        
        for audio_chunk in voice.synthesize(text):
            wav_file.writeframes(audio_chunk.audio_int16_bytes)
            
    return audio_stream.getvalue()
