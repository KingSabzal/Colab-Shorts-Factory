import os
import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description="Free AI Video Studio - Quick Start")
    parser.add_argument("--mode", type=str, choices=["manual", "viral"], default="viral",
                        help="Choose mode: 'manual' for custom topic, 'viral' for AI-generated")
    parser.add_argument("--topic", type=str, default="5 amazing facts about space exploration",
                        help="Topic to use (only for manual mode)")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(" 🎬 Free AI Video Studio - Quick Start")
    print("=" * 60)
    
    if args.mode == "viral":
        print("\n🔍 Fetching global trends...")
        from utility.trend.viral_title_generator import get_raw_trend, generate_viral_title_with_local_llm
        
        raw_topic = get_raw_trend()
        print(f"📌 Raw Trend Selected: '{raw_topic}'")
        print("🧠 Local AI is crafting the perfect viral title (downloading model on first run)...")
        
        topic = generate_viral_title_with_local_llm(raw_topic)
        print(f"🚀 AI-Generated Viral Title: '{topic}'\n")
    else:
        topic = args.topic
        print(f"\n📝 Manual Topic: '{topic}'\n")

    print("=" * 60)
    print(f"🎬 Starting video generation pipeline for: '{topic}'")
    print("=" * 60)
    
    try:
        subprocess.run([sys.executable, "app.py", topic], check=True)
        print("\n✅ Pipeline execution finished successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ An error occurred during video generation. Exit code: {e.returncode}")
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted by user.")

if __name__ == "__main__":
    main()
