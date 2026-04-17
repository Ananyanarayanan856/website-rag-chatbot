from faster_whisper import WhisperModel

print("Downloading STT model...")
WhisperModel("tiny.en", device="cpu", compute_type="int8")
print("Done! Model is cached and ready.")