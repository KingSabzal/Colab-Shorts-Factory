# 🎬 Colab Shorts Factory

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KingSabzal/Colab-Shorts-Factory/blob/main/run_colab.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

An advanced, fully automated AI video studio that turns a simple text topic into a fully edited, voice-overed, and captioned viral Short/Reel. 

Built for both **Google Colab (Cloud - Free)** and **Local Windows/Linux/Mac** environments. Features smart fallbacks, local AI models, and 2026-standard editing techniques.

---

## ✨ Key Features

### 🧠 Smart AI with Ultimate Fallback
- **Cloud First:** Automatically tries OpenRouter → Gemini → Groq → OpenAI.
- **Offline Fallback:** If all cloud APIs fail, uses **Local LLM (Qwen 2.5)** - works 100% offline.
- **Viral Title Generator:** Uses Local LLM to craft click-worthy titles based on 2026 golden rules.

### 🎙️ Emotion-Aware Voiceovers
- **Suno Bark (Local):** Generates natural voice with real emotions (sad, happy, excited, curious).
- **EdgeTTS (Free):** High-quality Microsoft voices in 50+ languages.
- **ElevenLabs (Premium):** Studio-grade voice cloning.

### 🎵 AI Background Music & Professional Ducking
- **MusicGen (Local):** Generates 2026-style Lo-Fi/Cinematic music automatically.
- **MuAPI (Optional):** Premium Suno AI integration for custom tracks.
- **Audio Ducking:** Professionally lowers music volume when the voice is speaking (2026 standard).

### 📝 6 Viral Caption Styles (2026 Trends)
*Each style automatically uses its own signature font for maximum engagement:*
| Style | Signature Font | Best For |
|-------|----------------|----------|
| **Hormozi** | Impact | Highest engagement, bold yellow/white |
| **Card** | Helvetica / Arial | Best readability on any background |
| **Neon** | Arial-Bold | Gen-Z aesthetic, glowing effect |
| **Minimal** | Helvetica / Arial | Professional, clean |
| **Karaoke** | Impact | High retention, word highlighting |
| **Comic** | Comic Sans MS | Entertainment, playful tone |

### 🎥 Smart B-Roll Sourcing
- **Pexels API (Free):** Stock footage from millions of videos.
- **MuAPI (Premium):** AI-generated video via Veo3, Sora, Kling, Seedance.

### 🎬 Moving Watermark
- Semi-transparent, gently floating watermark.
- Protects your content from unauthorized copying.
- Fully customizable (text, color, opacity).

### 📊 Auto Metadata Generator (2026 SEO)
Automatically generates optimized content for:
- **YouTube:** Title, Description, Tags (one per line), Category.
- **TikTok:** Caption with exactly 5 viral hashtags.
- **Instagram:** Caption with 10 strategic hashtags + dual CTA.

---

## 🚀 Quick Start

### Option 1: Google Colab (Recommended - Free)
Run the entire pipeline directly in your browser. No installation required!

👉 **[Open in Google Colab](https://colab.research.google.com/github/KingSabzal/Colab-Shorts-Factory/blob/main/run_colab.py)**

### Option 2: Local Installation (Windows/Linux/Mac)

#### Prerequisites
- Python 3.8+
- FFmpeg & ImageMagick (auto-installed on Windows)
- **NVIDIA GPU recommended** (for Local AI models like Bark, MusicGen, Qwen)
  - Minimum: 8GB VRAM (RTX 3060 or higher)
  - CPU fallback is available but slower.

#### Setup
```bash
# 1. Clone the repository
git clone https://github.com/KingSabzal/Colab-Shorts-Factory.git
cd Colab-Shorts-Factory

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your configuration file
cp .env.example .env

# 4. Edit .env and add your API keys
# At minimum: PEXELS_API_KEY + one LLM key (Gemini recommended - free)

#### Usage
**Interactive Mode (Recommended):**
```bash
python start.py

Then choose:
- `1` - Enter topic manually
- `2` - Auto-generate viral title from global trends

**Direct Mode:**
```bash
python app.py "5 amazing facts about space exploration"

Output: 5-amazing-facts-about-space-exploration.mp4 + metadata/ folder with SEO content.
