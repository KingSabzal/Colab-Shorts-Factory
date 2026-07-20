import os
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile as wavfile
import numpy as np

def generate_local_music(prompt: str, is_landscape: bool = False, output_path: str = "background_music.wav"):
    """
    Generates background music locally using MusicGen (via Transformers).
    This bypasses the unstable audiocraft library and works natively in Colab.
    """
    print(f"🎵 Generating local music using MusicGen for: '{prompt}'")
    model_id = "facebook/musicgen-small"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    print("📥 Loading MusicGen model (this may take a minute on first run)...")
    processor = AutoProcessor.from_pretrained(model_id)
    model = MusicgenForConditionalGeneration.from_pretrained(model_id).to(device)
    
    # Force a safe duration (e.g., 30 seconds = 1500 tokens at 50Hz)
    # This prevents the "max_new_tokens must be > 0" bug caused by boolean is_landscape
    duration = 30
    max_new_tokens = int(duration * 50)
    
    inputs = processor(
        text=[prompt],
        padding=True,
        return_tensors="pt",
    ).to(device)
    
    print("🎼 Generating audio...")
    audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True, guidance_scale=3.0)
    
    # Convert to numpy and save as 16-bit PCM WAV
    sampling_rate = model.config.audio_encoder.sampling_rate
    audio = audio_values[0, 0].cpu().numpy()
    audio = np.int16(audio / np.max(np.abs(audio)) * 32767)
    
    wavfile.write(output_path, sampling_rate, audio)
    print(f"✅ Local music generated and saved to: {output_path}")
    return output_path
