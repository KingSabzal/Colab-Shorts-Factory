# 🎬 Colab Shorts Factory

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](YOUR_COLAB_LINK_HERE)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

An advanced, fully automated AI video studio that turns a simple text topic into a fully edited, voice-overed, and captioned viral Short/Reel.

Built for both **Google Colab (Cloud - Free)** and **Local Windows/Linux/Mac** environments. Features smart fallbacks, local AI models, and 2026-standard editing techniques.

---

## ✨ Key Features

### 🧠 Smart AI with Ultimate Fallback
- **Cloud First:** Automatically tries OpenRouter → Gemini → Groq → OpenAI
- **Offline Fallback:** If all cloud APIs fail, uses **Local LLM (Qwen 2.5)** - works 100% offline
- **Viral Title Generator:** Uses Local LLM to craft click-worthy titles based on 2026 golden rules

### 🎙️ Emotion-Aware Voiceovers
- **Suno Bark (Local):** Generates natural voice with real emotions (sad, happy, excited, curious)
- **EdgeTTS (Free):** High-quality Microsoft voices in 50+ languages
- **ElevenLabs (Premium):** Studio-grade voice cloning

### 🎵 AI Background Music & Professional Ducking
- **MusicGen (Local):** Generates 2026-style Lo-Fi/Cinematic music automatically
- **MuAPI (Optional):** Premium Suno AI integration for custom tracks
- **Audio Ducking:** Professionally lowers music when voice is speaking (2026 standard)

### 📝 6 Viral Caption Styles (2026 Trends)
| Style | Font | Best For |
|-------|------|----------|
| **Hormozi** | Impact | Highest engagement, bold yellow/white |
| **Card** | Helvetica | Best readability on any background |
| **Neon** | Arial-Bold | Gen-Z aesthetic, glowing effect |
| **Minimal** | Helvetica | Professional, clean |
| **Karaoke** | Impact | High retention, word highlighting |
| **Comic** | Comic Sans | Entertainment, playful tone |

### 🎥 Smart B-Roll Sourcing
- **Pexels API (Free):** Stock footage from millions of videos
- **MuAPI (Premium):** AI-generated video via Veo3, Sora, Kling, Seedance

### 🎬 Moving Watermark
- Semi-transparent, gently floating watermark
- Protects your content from unauthorized copying
- Fully customizable (text, color, opacity)

### 📊 Auto Metadata Generator (2026 SEO)
Automatically generates optimized content for:
- **YouTube:** Title, Description, Tags (one per line), Category
- **TikTok:** Caption with 5 viral hashtags
- **Instagram:** Caption with 10 strategic hashtags + dual CTA

### 🎯 Smart Topic Selection
- **Manual Mode:** Enter your own topic
- **Auto-Trend Mode:** Fetches global viral trends and uses Local LLM to craft perfect viral titles

---

## 🚀 Quick Start

### Option 1: Google Colab (Recommended - Free)
Run the entire pipeline directly in your browser. No installation required!

👉 **[Open in Google Colab](YOUR_COLAB_LINK_HERE)**

### Option 2: Local Installation (Windows/Linux/Mac)

#### Prerequisites
- Python 3.8+
- FFmpeg & ImageMagick (auto-installed on Windows)
- **NVIDIA GPU recommended** (for Local AI models like Bark, MusicGen, Qwen)
  - Minimum: 8GB VRAM (RTX 3060 or higher)
  - CPU fallback available but slower

#### Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/Colab-Shorts-Factory.git
cd Colab-Shorts-Factory

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your configuration file
cp .env.example .env

# 4. Edit .env and add your API keys
# At minimum: PEXELS_API_KEY + one LLM key (Gemini recommended - free)

Usage
Interactive Mode (Recommended):
python start.py

Then choose:
1 - Enter topic manually
2 - Auto-generate viral title from global trends
Direct Mode:
python app.py "5 amazing facts about space exploration"
Output: 5-amazing-facts-about-space-exploration.mp4 + metadata/ folder with SEO content
⚙️ Configuration
All settings are in the .env file. Key configurations:
LLM & Fallback
LLM_PROVIDER=auto  # Tries cloud → falls back to local Qwen if offline
Text-to-Speech
TTS_PROVIDER=local  # Options: edgetts, elevenlabs, local (Bark with emotions)
LOCAL_TTS_VOICE=v2/en_speaker_6
Background Music
Captions
CAPTION_STYLE=hormozi  # Options: hormozi, card, neon, minimal, karaoke, comic
CAPTION_POSITION=bottom_center
Moving Watermark
WATERMARK_ENABLED=true
WATERMARK_TEXT=@YourChannelID
WATERMARK_OPACITY=0.3
📁 Project Structure
Colab-Shorts-Factory/
├── app.py                      # Main pipeline orchestrator
├── start.py                    # Interactive CLI for topic selection
├── requirements.txt            # Python dependencies
├── .env.example                # Configuration template
├── README.md                   # This file
├── INSTALL_WINDOWS.md          # Windows-specific setup guide
├── LICENSE                     # MIT License
│
├── utility/
│   ├── config.py               # Configuration manager
│   ├── pipeline_manager.py     # Stage tracking & checkpoints
│   ├── muapi_client.py         # MuAPI integration
│   │
│   ├── script/
│   │   └── script_generator.py # LLM script generation with fallback
│   │
│   ├── audio/
│   │   ├── audio_generator.py  # TTS orchestrator
│   │   └── audio_ducker.py     # Professional audio ducking
│   │
│   ├── tts/
│   │   ├── edgetts_tts.py      # EdgeTTS integration
│   │   ├── elevenlabs_tts.py   # ElevenLabs integration
│   │   ├── local_tts.py        # Bark TTS with emotions
│   │   └── emotion_analyzer.py # Sentiment analysis for tone
│   │
│   ├── stt/
│   │   ├── whisper_stt.py      # Local Whisper STT
│   │   └── deepgram_stt.py     # Deepgram cloud STT
│   │
│   ├── captions/
│   │   ├── timed_captions_generator.py
│   │   └── caption_styler.py   # 6 viral caption styles (2026)
│   │
│   ├── music/
│   │   └── local_music_generator.py  # MusicGen integration
│   │
│   ├── llm/
│   │   └── local_llm_client.py # Local Qwen model for offline fallback
│   │
│   ├── trend/
│   │   └── viral_title_generator.py  # AI-powered viral titles
│   │
│   ├── metadata/
│   │   └── metadata_generator.py     # SEO metadata for YouTube/TikTok/Instagram
│   │
│   ├── video/
│   │   ├── background_video_generator.py
│   │   └── video_search_query_generator.py
│   │
│   └── render/
│       ├── render_engine.py    # MoviePy renderer
│       └── remotion_renderer.py # React/Remotion renderer (advanced)
│
└── remotion-composer/          # React-based renderer (optional)
    └── src/
🔑 Required API Keys
Service
Purpose
Cost
Get Key
Pexels
Stock video footage
Free
pexels.com/api
Gemini
Script generation
Free
aistudio.google.com
OpenRouter
Smart fallback
Free tier
openrouter.ai
Groq
Smart fallback
Free tier
console.groq.com
MuAPI
Premium AI video/music
Paid
muapi.ai
Minimum required: Pexels + one LLM key (Gemini recommended)
🎯 Output
After running the pipeline, you get:
Video File: your-topic-name.mp4
Fully edited with B-roll footage
Professional voiceover with emotions
2026-style captions
Background music with ducking
Moving watermark (if enabled)
Metadata Folder: metadata/
youtube_title.txt - SEO-optimized title
youtube_description.txt - Hook + summary + hashtags
youtube_tags.txt - 12 tags (one per line)
youtube_category.txt - Best category
tiktok_caption.txt - Viral caption + 5 hashtags
instagram_caption.txt - Engaging caption + 10 hashtags
🤝 Contributing
Contributions are welcome! Please:
Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments
This project is a heavily modified and enhanced fork of SamurAIGPT/Text-To-Video-AI.
Special thanks to:
Meta for MusicGen and Llama models
Suno for Bark TTS
Pexels for free stock footage
Hugging Face for model hosting
🌟 Support
If you find this project useful, please consider giving it a star! ⭐
Your support helps us continue improving this project and keeping it 100% free and open-source.
Made with ❤️ for content creators worldwide
