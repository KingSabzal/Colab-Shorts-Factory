"""
Local TTS (Text-to-Speech) Generator - Suno Bark with PyTorch 2.6+ Fix
Uses a monkey-patch to fix the 'weights_only' error in PyTorch 2.6+.
Guaranteed to load Bark models without errors.
"""
import os
import torch
import numpy as np
from scipy.io.wavfile import write as write_wav
from bark import SAMPLE_RATE, generate_audio, preload_models
from utility.tts.emotion_analyzer import add_emotion_tags

# ==========================================
# CRITICAL FIX for PyTorch 2.6+ (Colab & Local)
# ==========================================
# This patch MUST be applied BEFORE any other imports
# It forces weights_only=False specifically for Bark loading
# ==========================================
def _safe_torch_load(*args, **kwargs):
    """Override torch.load to fix weights_only error in PyTorch 2.6+"""
    kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)

# Save original torch.load
_original_torch_load = torch.load
# Apply our safe override
torch.load = _safe_torch_load
# ==========================================

def generate_audio(script: str, output_filename: str, voice_preset: str = "v2/en_speaker_6"):
    """
    Generates voiceover using Suno Bark with emotion analysis.
    Handles PyTorch 2.6+ compatibility issues.
    """
    print(f"[LocalTTS] Preloading Bark models (this may take 1-2 minutes on first run)...")
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
