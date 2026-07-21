"""
Audio Generator - TTS Orchestration
Supports: EdgeTTS (free, high-quality) and ElevenLabs (premium)
"""
import os
import asyncio


async def generate_audio(script: str, output_filename: str):
    """
    Generate audio using the configured TTS provider.
    """
    from utility.config import get_config
    
    config = get_config()
    tts_provider = config.get_tts_provider()
    
    print(f"\n--- STAGE 2: Generating Voiceover ---")
    print(f"🎙️ Using TTS Provider: {tts_provider}")
    
    if tts_provider == 'edgetts':
        from utility.tts.edgetts_tts import generate_audio as edgetts_audio
        await edgetts_audio(script, output_filename)
        
    elif tts_provider == 'elevenlabs':
        from utility.tts.elevenlabs_tts import generate_audio as elevenlabs_audio
        await elevenlabs_audio(script, output_filename)
        
    else:
        raise ValueError(f"Unknown TTS provider: {tts_provider}. Supported: edgetts, elevenlabs")
    
    print(f"[PipelineManager] Checkpoint saved: stage='2_voiceover'")
