"""
Music Generator - Royalty-Free Music from Multiple Sources
Priority: YouTube (NCS channels) → Pixabay → Free Music Archive → SoundHelix → Tone Generator
Guaranteed to find music - never falls back to silent audio.
"""
import os
import requests
import random
import subprocess
import sys
import numpy as np
import scipy.io.wavfile as wavfile


def generate_local_music(prompt: str, is_landscape: bool = False, output_path: str = "background_music.wav"):
    """
    Downloads royalty-free music from multiple sources.
    Priority: YouTube → Pixabay → FMA → SoundHelix → Tone Generator
    """
    print(f"🎵 Searching for royalty-free music for: '{prompt}'")
    
    # 1. Try YouTube first
    print("\n1️⃣ Trying YouTube (NoCopyrightSounds & similar channels)...")
    if _download_from_youtube(prompt, output_path):
        return output_path
    
    # 2. Try Pixabay
    print("\n2️⃣ Trying Pixabay...")
    api_key = os.getenv('PEXELS_API_KEY')
    if api_key and api_key != 'your_pexels_api_key_here':
        if _download_from_pixabay(api_key, prompt, output_path):
            return output_path
    else:
        print("⚠️ PEXELS_API_KEY not set, skipping Pixabay")
    
    # 3. Try Free Music Archive
    print("\n3️⃣ Trying Free Music Archive...")
    if _download_from_fma(output_path):
        return output_path
    
    # 4. Try SoundHelix (guaranteed direct MP3 URLs)
    print("\n4️⃣ Using SoundHelix royalty-free MP3s...")
    if _download_from_soundhelix(output_path):
        return output_path
    
    # 5. Absolute last resort: Generate a pleasant tone (never silent)
    print("\n5️⃣ Generating pleasant background tone...")
    return _generate_pleasant_tone(output_path)


def _download_from_youtube(prompt: str, output_path: str) -> bool:
    """Download from YouTube NoCopyright channels using yt-dlp"""
    try:
        # Install yt-dlp if not available
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'yt-dlp'], check=True, 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # List of YouTube playlist IDs with royalty-free music
        youtube_playlists = [
            "https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK",  # NCS
            "https://www.youtube.com/playlist?list=PLj7ZTD1_2xK_5K8z8z8z8z8z8z8z8z8z8",  # Audio Library
        ]
        
        # Select a random playlist
        playlist_url = random.choice(youtube_playlists)
        
        print(f"📥 Downloading from YouTube playlist...")
        
        # Use yt-dlp to download a random video from playlist
        cmd = [
            'yt-dlp',
            '-f', 'bestaudio/best',
            '--extract-audio',
            '--audio-format', 'wav',
            '--audio-quality', '0',
            '-o', output_path,
            '--random-playlist',
            '--no-playlist',
            playlist_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0 and os.path.exists(output_path):
            print(f"✅ Music downloaded from YouTube")
            return True
        else:
            print(f"⚠️ YouTube download failed")
            return False
            
    except Exception as e:
        print(f"⚠️ YouTube download error: {e}")
        return False


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
            return False
        
        music_tracks = [hit for hit in data['hits'] if hit.get('type') == 'music']
        if not music_tracks:
            return False
        
        selected_track = random.choice(music_tracks[:5])
        music_url = selected_track.get('previewURL')
        
        if not music_url:
            return False
        
        print(f"📥 Downloading: {selected_track.get('tags', 'Unknown')}")
        
        music_response = requests.get(music_url, timeout=30)
        music_response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(music_response.content)
        
        print(f"✅ Music downloaded from Pixabay")
        return True
        
    except Exception as e:
        print(f"️ Pixabay failed: {e}")
        return False


def _download_from_fma(output_path: str) -> bool:
    """Download from Free Music Archive"""
    fma_tracks = [
        "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/ccCommunity/Kai_Engel/Satin/Kai_Engel_-_04_-_Sentinel.mp3",
        "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/Tours/Enthusiast/Tours_-_01_-_Enthusiast.mp3",
        "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/ccCommunity/Chad_Crouch/Arps/Chad_Crouch_-_Elipses.mp3",
    ]
    
    try:
        selected_url = random.choice(fma_tracks)
        response = requests.get(selected_url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Music downloaded from FMA")
        return True
    except Exception as e:
        print(f"⚠️ FMA failed: {e}")
        return False


def _download_from_soundhelix(output_path: str) -> bool:
    """Download from SoundHelix (guaranteed royalty-free MP3s)"""
    soundhelix_tracks = [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
    ]
    
    try:
        selected_url = random.choice(soundhelix_tracks)
        print(f"📥 Downloading from SoundHelix...")
        
        response = requests.get(selected_url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Music downloaded from SoundHelix")
        return True
    except Exception as e:
        print(f"⚠️ SoundHelix failed: {e}")
        return False


def _generate_pleasant_tone(output_path: str, duration: int = 30) -> str:
    """Generate a pleasant ambient tone as absolute last resort (never silent)"""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate a pleasant 220Hz (A3) ambient tone with harmonics
    tone = (0.3 * np.sin(2 * np.pi * 220 * t) + 
            0.15 * np.sin(2 * np.pi * 440 * t) +
            0.1 * np.sin(2 * np.pi * 330 * t))
    
    # Fade in/out to avoid clicks
    fade_samples = int(sample_rate * 2)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    tone[:fade_samples] *= fade_in
    tone[-fade_samples:] *= fade_out
    
    audio = np.int16(tone * 32767)
    wavfile.write(output_path, sample_rate, audio)
    print(f"✅ Generated pleasant ambient tone ({duration}s)")
    return output_path
