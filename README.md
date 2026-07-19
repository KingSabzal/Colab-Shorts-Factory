#  Colab Shorts Factory

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KingSabzal/Colab-Shorts-Factory/blob/main/run_colab.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

An advanced, fully automated AI video studio that turns a simple text topic into a fully edited, voice-overed, and captioned viral Short/Reel. 

Built for both **Google Colab (Cloud - Free)** and **Local Windows/Linux/Mac** environments. Features smart fallbacks, local AI models, and 2026-standard editing techniques.

---

##  Key Features

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
```
#### Usage

**Interactive Mode:**
```bash
python start.py
```
**Direct Mode:**
```bash
python app.py "5 amazing facts about space exploration"
```
---

## ⚙️ Configuration

All settings are configured via the `.env` file. Key configurations:

### LLM & Fallback
```env
LLM_PROVIDER=auto  # Tries cloud → falls back to local Qwen if offline
```

### Text-to-Speech
```env
TTS_PROVIDER=local  # Options: edgetts, elevenlabs, local (Bark with emotions)
LOCAL_TTS_VOICE=v2/en_speaker_6
```
---

### Background Music & Ducking
```env
LOCAL_MUSIC_ENABLED=true  # Auto-fallback to MusicGen if MuAPI missing
AUDIO_DUCKING_ENABLED=true  # Professional sidechain compression
```
### Captions
```env
CAPTION_STYLE=hormozi  # Options: hormozi, card, neon, minimal, karaoke, comic
CAPTION_POSITION=bottom_center
```
---

### Moving Watermark
```env
WATERMARK_ENABLED=true
WATERMARK_TEXT=@YourChannelID
WATERMARK_OPACITY=0.3
```
---

## 📁 Project Structure

```text
Colab-Shorts-Factory/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── .env.example
├── app.py                      # Main pipeline orchestrator
├── start.py                    # Interactive CLI for topic selection
├── run_colab.py                # Google Colab runner script
├── config.py                   # Global configuration manager
│
├── utility/
│   ├── __init__.py
│   ├── config/
│   │   └── config.py           # Configuration manager
│   ├── script/
│   │   ├── __init__.py
│   │   └── script_generator.py # LLM script generation with fallback
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── audio_generator.py  # TTS orchestrator
│   │   └── audio_ducker.py     # Professional audio ducking
│   ├── tts/
│   │   ├── __init__.py
│   │   ├── edgetts_tts.py      # EdgeTTS integration
│   │   ├── elevenlabs_tts.py   # ElevenLabs integration
│   │   └── local_tts.py        # Bark TTS with emotions
│   ├── stt/
│   │   ├── __init__.py
│   │   └── whisper_stt.py      # Local Whisper STT
│   ├── captions/
│   │   ├── __init__.py
│   │   ├── timed_captions_generator.py
│   │   └── caption_styler.py   # 6 viral caption styles (2026)
│   ├── music/
│   │   ├── __init__.py
│   │   └── local_music_generator.py  # MusicGen integration
│   ├── llm/
│   │   ├── __init__.py
│   │   └── local_llm_client.py # Local Qwen model for offline fallback
│   ├── metadata/
│   │   ├── __init__.py
│   │   └── metadata_generator.py     # SEO metadata generator
│   ├── video/
│   │   ├── __init__.py
│   │   ├── background_video_generator.py
│   │   └── video_search_query_generator.py
│   └── render/
│       ├── __init__.py
│       ├── render_engine.py    # MoviePy renderer
│       └── remotion_renderer.py # React/Remotion renderer (advanced)
│
└── remotion-composer/          # React-based renderer (optional)
    └── src/
        └── index.tsx
```
---

## 🔑 Required API Keys

| Service | Purpose | Cost | Get Key |
|---------|---------|------|---------|
| **Pexels** | Stock video footage | Free | [pexels.com/api](https://www.pexels.com/api/) |
| **Gemini** | LLM Script Generation | Free | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| **OpenRouter** | LLM Smart Fallback | Free tier | [openrouter.ai](https://openrouter.ai/keys) |
| **Groq** | LLM Smart Fallback | Free tier | [console.groq.com](https://console.groq.com/keys) |
| **OpenAI** | LLM Smart Fallback | Paid | [platform.openai.com](https://platform.openai.com/api-keys) |
| **MuAPI** | Premium AI Video & Music | Paid | [muapi.ai](https://muapi.ai/) |
| **ElevenLabs** | Premium Voiceover (TTS) | Paid | [elevenlabs.io](https://elevenlabs.io/) |
| **Deepgram** | Premium Speech-to-Text (STT) | Paid | [console.deepgram.com](https://console.deepgram.com/) |

**Minimum required to start:** Pexels + one free LLM key (Gemini recommended).
---

## 🎯 Output

After running the pipeline, you get:

1. **Video File:** `your-topic-name.mp4`
   - Fully edited with B-roll, voiceover, captions, and watermark.
2. **Metadata Folder:** `metadata/`
   - Ready-to-copy SEO files for YouTube, TikTok, and Instagram.
  ---

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.
*Copyright (c) 2026 KingSabzal*

---

## 🙏 Acknowledgments

This project is a heavily modified and enhanced fork of [SamurAIGPT/Text-To-Video-AI](https://github.com/SamurAIGPT/Text-To-Video-AI).

Special thanks to:
- **Meta** for MusicGen and Llama models
- **Suno** for Bark TTS
- **Pexels** for free stock footage
- **Hugging Face** for model hosting

---

## 🌟 Support

If you find this project useful, please consider giving it a star! ⭐

Your support helps us continue improving this project and keeping it 100% free and open-source.

---

**Made with ❤️ for content creators worldwide**
