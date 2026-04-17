import os
import io
import wave
import re
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
    Adds pauses after points in numbered/bulleted lists.
    """
    voice = get_voice()
    audio_stream = io.BytesIO()
    
    with wave.open(audio_stream, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes for 16-bit
        wav_file.setframerate(voice.config.sample_rate)
        
        # Split text by lines to process points separately
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Define silence periods (0.8s for list items, 0.3s for general paragraphs)
        pause_frames_long = int(voice.config.sample_rate * 0.8)
        silence_bytes_long = b'\x00' * (pause_frames_long * 2)
        
        pause_frames_short = int(voice.config.sample_rate * 0.3)
        silence_bytes_short = b'\x00' * (pause_frames_short * 2)
        
        for i, line in enumerate(lines):
            for audio_chunk in voice.synthesize(line):
                wav_file.writeframes(audio_chunk.audio_int16_bytes)
            
            # Insert long pause if this line is a numbered/bullet point
            if re.match(r'^(\d+\.|\*|-|•)\s+', line):
                wav_file.writeframes(silence_bytes_long)
            elif i < len(lines) - 1:
                wav_file.writeframes(silence_bytes_short)
            
    return audio_stream.getvalue()
