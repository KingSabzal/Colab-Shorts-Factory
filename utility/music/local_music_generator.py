"""
Local Music Generator - Royalty-Free Music from Pixabay
Downloads professional, copyright-free music that matches the video topic.
Uses the same API key as Pexels (no additional key required).
"""
import os
import requests
import random
import numpy as np
import scipy.io.wavfile as wavfile


def generate_local_music(prompt: str, is_landscape: bool = False, output_path: str = "background_music.wav"):
    """
    Downloads royalty-free music from Pixabay based on video topic.
    Falls back to other free sources if Pixabay fails.
    """
    print(f"🎵 Searching for royalty-free music for: '{prompt}'")
    
    # Get API key (same as Pexels)
    api_key = os.getenv('PEXELS_API_KEY')
    
    if not api_key or api_key == 'your_pexels_api_key_here':
        print("️ PEXELS_API_KEY not found. Creating silent audio fallback...")
        return _create_silent_audio(output_path)
    
    # Try Pixabay first
    success = _download_from_pixabay(api_key, prompt, output_path)
    
    if success:
        return output_path
    
    # Fallback: Try Free Music Archive (FMA)
    print("🔄 Trying Free Music Archive as fallback...")
    success = _download_from_fma(prompt, output_path)
    
    if success:
        return output_path
    
    # Final fallback: Silent audio
    print("⚠️ All music sources failed. Creating silent audio...")
    return _create_silent_audio(output_path)


def _download_from_pixabay(api_key: str, prompt: str, output_path: str) -> bool:
    """Download music from Pixabay API"""
    try:
        url = "https://pixabay.com/api/"
        params = {
            'key': api_key,
            'q': prompt,
            'type': 'music',
            'per_page': 20,
            'safesearch': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'hits' not in data or len(data['hits']) == 0:
            print("⚠️ No results from Pixabay")
            return False
        
        # Filter for music tracks
        music_tracks = [hit for hit in data['hits'] if hit.get('type') == 'music']
        
        if not music_tracks:
            print("️ No music tracks found in Pixabay results")
            return False
        
        # Select a random track from top results
        selected_track = random.choice(music_tracks[:5])
        music_url = selected_track.get('previewURL')
        
        if not music_url:
            print("⚠️ No preview URL found")
            return False
        
        print(f"📥 Downloading from Pixabay:")
        print(f"   Tags: {selected_track.get('tags', 'Unknown')}")
        print(f"   Artist: {selected_track.get('user', 'Unknown')}")
        print(f"   Duration: {selected_track.get('duration', 'Unknown')}s")
        
        # Download the music
        music_response = requests.get(music_url, timeout=30)
        music_response.raise_for_status()
        
        # Save to output path
        with open(output_path, 'wb') as f:
            f.write(music_response.content)
        
        print(f"✅ Music downloaded successfully from Pixabay")
        return True
        
    except Exception as e:
        print(f"⚠️ Pixabay download failed: {e}")
        return False


def _download_from_fma(prompt: str, output_path: str) -> bool:
    """Fallback: Download from Free Music Archive"""
    try:
        # FMA doesn't have a public API, so we use a curated list of CC0 music
        # These are direct links to Creative Commons Zero (public domain) music
        fma_tracks = [
            "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/ccCommunity/Kai_Engel/Satin/Kai_Engel_-_04_-_Sentinel.mp3",
            "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/Tours/Enthusiast/Tours_-_01_-_Enthusiast.mp3",
            "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/ccCommunity/Chad_Crouch/Arps/Chad_Crouch_-_Elipses.mp3",
        ]
        
        # Select a random track
        selected_url = random.choice(fma_tracks)
        
        print(f"📥 Downloading from Free Music Archive...")
        
        response = requests.get(selected_url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Music downloaded from Free Music Archive")
        return True
        
    except Exception as e:
        print(f"⚠️ FMA download failed: {e}")
        return False


def _create_silent_audio(output_path: str, duration: int = 30) -> str:
    """Create silent audio as final fallback"""
    sample_rate = 44100
    silent_audio = np.zeros(int(sample_rate * duration), dtype=np.int16)
    wavfile.write(output_path, sample_rate, silent_audio)
    print(f"✅ Created silent audio ({duration}s)")
    return output_path
