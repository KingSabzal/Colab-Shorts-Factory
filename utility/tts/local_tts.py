import os
import torch
import numpy as np

# ==========================================
# CRITICAL FIX for PyTorch 2.6+ in Colab/Local
# Bark's internal torch.load fails with weights_only=True (new default).
# This monkey-patch forces weights_only=False specifically for Bark loading.
# ==========================================
_original_torch_load = torch.load
def _safe_torch_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)
torch.load = _safe_torch_load
# ==========================================

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from utility.tts.emotion_analyzer import add_emotion_tags

def generate_audio(script: str, output_filename: str, voice_preset: str = "v2/en_speaker_6"):
    print(f"[LocalTTS] Preloading Bark models (first time may take 1-2 minutes)...")
    preload_models()
    
    print(f"[LocalTTS] Analyzing emotions and adding tags to script...")
    tagged_script = add_emotion_tags(script)
    print(f"[LocalTTS] Generating audio with preset: {voice_preset}")
    
    # Generate audio
    audio_array = generate_audio(tagged_script, history_prompt=voice_preset)
    
    # Save audio
    write_wav(output_filename, SAMPLE_RATE, audio_array)
    print(f"✅ Local voiceover generated and saved to: {output_filename}")
    return output_filename
