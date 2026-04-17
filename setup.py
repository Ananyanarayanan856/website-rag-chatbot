import os
import sys
from faster_whisper import WhisperModel
from huggingface_hub import hf_hub_download

def setup_whisper():
    """Initialize and cache the Faster-Whisper STT model"""
    try:
        print("--- STT Setup ---")
        print("Downloading/Loading Whisper model (tiny.en)...")
        # Initializing the model automatically handles the download/caching
        WhisperModel("tiny.en", device="cpu", compute_type="int8")
        print("[OK] Whisper model is cached and ready.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to setup Whisper: {e}", file=sys.stderr)
        return False

def setup_piper():
    """Download Piper TTS voice model from Hugging Face"""
    print("\n--- TTS Setup ---")
    model_dir = "chatbot/text_to_speech/models"
    os.makedirs(model_dir, exist_ok=True)
    
    files_to_download = [
        "en/en_US/lessac/medium/en_US-lessac-medium.onnx",
        "en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
    ]
    
    try:
        for file in files_to_download:
            print(f"Downloading {os.path.basename(file)}...")
            hf_hub_download(
                repo_id="rhasspy/piper-voices",
                filename=file,
                local_dir=model_dir,
                local_dir_use_symlinks=False
            )
        print("[OK] Piper voice models downloaded successfully!")
        return True
    except Exception as e:
        print(f"[ERROR] Error downloading Piper models: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    print("Starting AI Model Setup...")
    print("=" * 30)
    
    whisper_success = setup_whisper()
    piper_success = setup_piper()
    
    print("=" * 30)
    if whisper_success and piper_success:
        print("Full environment setup complete!")
        sys.exit(0)
    else:
        print("Setup failed for one or more components.")
        sys.exit(1)