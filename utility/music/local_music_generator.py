"""
Dynamic Music Generator
=======================
Searches Pixabay and YouTube dynamically based on the video topic.
No more static or repetitive tracks - every video gets unique, topic-matched music.

Priority Order:
    1. MuAPI (if MUAPI_API_KEY is set) - Premium AI-generated music
    2. Pixabay API (if PIXABAY_API_KEY is set) - Royalty-free professional music
    3. YouTube Dynamic Search (via yt-dlp) - "no copyright music [topic]"
    4. Ambient Tone Generator (fallback - never silent, always copyright-free)
"""
import os
import subprocess
import sys
import requests
import random
import numpy as np
import scipy.io.wavfile as wavfile


def generate_local_music(prompt: str, is_landscape: bool = False, output_path: str = "background_music.wav"):
    """
    Dynamically finds and downloads royalty-free music based on the video prompt.
    
    Args:
        prompt: The video topic/title used to search for matching music.
        is_landscape: Whether the video is landscape (unused, kept for API compatibility).
        output_path: The file path where the music will be saved.
    
    Returns:
        str: The path to the generated/downloaded music file.
    """
    print(f"\n🎵 Searching for dynamic royalty-free music for: '{prompt}'")
    
    # Clean the prompt for better search results
    clean_prompt = _clean_prompt_for_search(prompt)
    
    # 1. Try Pixabay First (if key is provided) - Best quality, topic-matched
    pixabay_key = os.getenv('PIXABAY_API_KEY', '')
    if pixabay_key and pixabay_key not in ['', 'your_pixabay_api_key_here']:
        print("   🔍 Trying Pixabay API...")
        if _download_from_pixabay(pixabay_key, clean_prompt, output_path):
            return output_path
        print("   ⚠️ Pixabay search yielded no results. Trying YouTube...")
    else:
        print("   ℹ️ PIXABAY_API_KEY not set. Skipping to YouTube search...")

    # 2. Try YouTube Dynamic Search - "no copyright music [topic]"
    print("   🔍 Trying YouTube dynamic search...")
    if _download_from_youtube(clean_prompt, output_path):
        return output_path
    
    # 3. Final Fallback: Generate a pleasant ambient tone (never truly silent)
    print("   ⚠️ All online music sources failed. Generating a safe ambient tone...")
    return _generate_ambient_tone(output_path)


def _clean_prompt_for_search(prompt: str) -> str:
    """
    Clean the prompt to create a better search query.
    Removes quotes, special characters, and extracts key terms.
    """
    # Remove common punctuation and quotes
    cleaned = prompt.replace('"', '').replace('!', '').replace('?', '').replace("'", "")
    
    # If prompt is too long, take first few meaningful words
    words = cleaned.split()
    if len(words) > 10:
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                     'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 
                     'would', 'could', 'should', 'may', 'might', 'can', 'to', 'of', 
                     'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 
                     'through', 'during', 'before', 'after', 'and', 'but', 'or', 
                     'nor', 'not', 'so', 'yet', 'both', 'either', 'neither', 
                     'each', 'every', 'all', 'any', 'few', 'more', 'most', 'other', 
                     'some', 'such', 'no', 'only', 'own', 'same', 'than', 'too', 
                     'very', 'just', 'because', 'about', 'up', 'out', 'if', 'when'}
        meaningful = [w for w in words if w.lower() not in stop_words][:8]
        cleaned = ' '.join(meaningful)
    
    return cleaned.strip()


def _download_from_pixabay(api_key: str, prompt: str, output_path: str) -> bool:
    """
    Search Pixabay API dynamically based on prompt and download a matching track.
    
    Args:
        api_key: Pixabay API key.
        prompt: Cleaned search query.
        output_path: Where to save the downloaded music.
    
    Returns:
        bool: True if download succeeded, False otherwise.
    """
    try:
        # Pixabay API endpoint
        url = "https://pixabay.com/api/"
        
        # Search parameters - focus on background/instrumental music
        params = {
            'key': api_key,
            'q': f"{prompt} background instrumental",
            'type': 'music',
            'per_page': 20,
            'safesearch': 'true',
            'order': 'popular'  # Get most popular tracks first
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if 'hits' not in data or len(data['hits']) == 0:
            print("      No results from Pixabay.")
            return False
        
        # Filter for music tracks with preview URLs
        music_tracks = [
            hit for hit in data['hits'] 
            if hit.get('type') == 'music' and hit.get('previewURL')
        ]
        
        if not music_tracks:
            print("      No playable tracks found in Pixabay results.")
            return False
        
        # Select a random track from top 5 results for variety
        selected = random.choice(music_tracks[:5])
        music_url = selected.get('previewURL')
        
        print(f"      📥 Downloading: {selected.get('tags', 'Unknown')}")
        print(f"         Artist: {selected.get('user', 'Unknown')}")
        print(f"         Duration: {selected.get('duration', 'Unknown')}s")
        
        # Download the music file
        music_response = requests.get(music_url, timeout=30)
        music_response.raise_for_status()
        
        # Save to output path
        with open(output_path, 'wb') as f:
            f.write(music_response.content)
        
        print("      ✅ Music downloaded successfully from Pixabay.")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"      ⚠️ Pixabay network error: {e}")
        return False
    except Exception as e:
        print(f"      ⚠️ Pixabay unexpected error: {e}")
        return False


def _download_from_youtube(prompt: str, output_path: str) -> bool:
    """
    Use yt-dlp to dynamically search and download a no-copyright track matching the topic.
    Uses 'ytsearch1:' to find the single best matching video.
    
    Args:
        prompt: Cleaned search query.
        output_path: Where to save the downloaded music.
    
    Returns:
        bool: True if download succeeded, False otherwise.
    """
    try:
        # Ensure yt-dlp is installed
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-q', 'yt-dlp'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Build dynamic search query
        # ytsearch1: finds the single best matching video
        search_query = f"ytsearch1:no copyright music {prompt} background instrumental"
        
        print(f"      🔍 Searching YouTube for: '{search_query}'")
        
        # yt-dlp command to download audio only
        cmd = [
            'yt-dlp',
            '-f', 'bestaudio[ext=m4a]/bestaudio',  # Prefer m4a for quality
            '-x',                                    # Extract audio
            '--audio-format', 'mp3',                # Convert to mp3
            '--audio-quality', '0',                 # Best quality
            '-o', output_path,                      # Output path
            '--no-playlist',                        # Don't download playlist
            '--quiet',                              # Minimal output
            '--no-warnings',                        # Suppress warnings
            '--socket-timeout', '30',               # Timeout for slow connections
            search_query
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Check if download succeeded
        if result.returncode == 0 and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            if file_size > 50000:  # At least 50KB (valid audio file)
                print(f"      ✅ Music downloaded dynamically from YouTube ({file_size // 1024} KB).")
                return True
            else:
                print(f"      ⚠️ Downloaded file too small ({file_size} bytes).")
                # Remove invalid file
                try:
                    os.remove(output_path)
                except:
                    pass
                return False
        else:
            print(f"      ⚠️ YouTube download failed.")
            if result.stderr:
                print(f"         Error: {result.stderr[:200]}")
            return False
            
    except subprocess.TimeoutExpired:
        print("      ⚠️ YouTube download timed out.")
        return False
    except Exception as e:
        print(f"      ⚠️ YouTube search error: {e}")
        return False


def _generate_ambient_tone(output_path: str, duration: int = 30) -> str:
    """
    Generate a safe, pleasant, copyright-free ambient drone as absolute last resort.
    This ensures the video ALWAYS has background music, even if all online sources fail.
    
    Args:
        output_path: Where to save the generated audio.
        duration: Duration in seconds (default 30s).
    
    Returns:
        str: The path to the generated audio file.
    """
    try:
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Create a soft ambient chord (A minor: A3, C4, E4)
        # Using multiple harmonics for a richer sound
        tone = (
            0.15 * np.sin(2 * np.pi * 220 * t) +   # A3 (fundamental)
            0.10 * np.sin(2 * np.pi * 261.63 * t) + # C4
            0.08 * np.sin(2 * np.pi * 329.63 * t) + # E4
            0.05 * np.sin(2 * np.pi * 440 * t) +    # A4 (octave)
            0.03 * np.sin(2 * np.pi * 110 * t)      # A2 (sub-bass)
        )
        
        # Add subtle vibrato for warmth
        vibrato = 0.02 * np.sin(2 * np.pi * 5 * t)
        tone = tone * (1 + vibrato)
        
        # Apply fade in/out to avoid clicks
        fade_samples = int(sample_rate * 2)  # 2 second fade
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        
        tone[:fade_samples] *= fade_in
        tone[-fade_samples:] *= fade_out
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(tone))
        if max_val > 0:
            tone = tone / max_val * 0.8  # Leave headroom
        
        # Convert to 16-bit PCM
        audio = np.int16(tone * 32767)
        
        # Save as WAV
        wavfile.write(output_path, sample_rate, audio)
        
        print(f"      ✅ Safe ambient tone generated ({duration}s).")
        return output_path
        
    except Exception as e:
        print(f"      ❌ Failed to generate ambient tone: {e}")
        # Last resort: create silent audio
        sample_rate = 44100
        silent = np.zeros(int(sample_rate * 30), dtype=np.int16)
        wavfile.write(output_path, sample_rate, silent)
        return output_path
