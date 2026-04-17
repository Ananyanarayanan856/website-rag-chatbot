from huggingface_hub import hf_hub_download
import os
import sys

def download_piper_model():
    """Download Piper TTS voice model from Hugging Face"""
    model_dir = "chatbot/text_to_speech/models"
    os.makedirs(model_dir, exist_ok=True)
    
    files_to_download = [
        "en/en_US/lessac/medium/en_US-lessac-medium.onnx",
        "en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
    ]
    
    try:
        for file in files_to_download:
            print(f"Downloading {file.split('/')[-1]}...")
            hf_hub_download(
                repo_id="rhasspy/piper-voices",
                filename=file,
                local_dir=model_dir,
                local_dir_use_symlinks=False
            )
        print("[OK] Voice models downloaded successfully!")
        return True
    except Exception as e:
        print(f"[ERROR] Error downloading models: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    print("Setting up Piper TTS voice models...")
    success = download_piper_model()
    sys.exit(0 if success else 1)