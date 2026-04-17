from faster_whisper import WhisperModel
import tempfile
import os

print("Loading STT model...")
# Keep this at the module level so it only loads once when the app starts
model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
print("Model ready!")

async def process_audio_chunk(file_bytes: bytes) -> str:
    """Saves the audio chunk temporarily, transcribes it, and cleans up."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        segments, _ = model.transcribe(
            tmp_path,
            language="en",
            beam_size=1,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=300)
        )
        text = " ".join(s.text.strip() for s in segments)
    finally:
        # Ensure the temp file is deleted even if an error occurs
        os.remove(tmp_path)
        
    return text if text else "No speech detected."