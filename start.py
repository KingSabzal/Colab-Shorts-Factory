"""
Colab Shorts Factory - Interactive Starter (Global 24h Trends Edition)
======================================================================
Fetches REAL global trends from the last 24 hours across ALL niches.
Generates 10 viral titles in the user's chosen language.
"""
import os
import sys
import json
import random
import requests
import xml.etree.ElementTree as ET

project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

from utility.config import get_config


def fetch_global_24h_trends():
    """
    Fetch REAL trending topics from the last 24 hours using Google Trends RSS.
    Queries multiple regions to ensure a truly global, diverse mix (not just AI).
    """
    print("\n🌍 Fetching REAL global trends from the last 24 hours...")
    
    # Query multiple major regions to get a diverse global mix
    regions = ['US', 'GB', 'CA', 'AU', 'IN']
    all_trends = set()
    
    for geo in regions:
        try:
            url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                for item in root.findall('.//item'):
                    title = item.find('title').text
                    # Clean up title (remove view counts or extra info)
                    clean_title = title.split(' - ')[0].strip()
                    if len(clean_title) > 4:
                        all_trends.add(clean_title)
        except Exception:
            continue
    
    if len(all_trends) >= 10:
        trends_list = list(all_trends)
        random.shuffle(trends_list)
        print(f"   ✅ Successfully fetched {len(trends_list)} diverse global trends!")
        return trends_list[:15]
    else:
        print("   ⚠️ Could not fetch live trends. Using diverse global fallback topics...")
        return _get_diverse_fallback_trends()


def _get_diverse_fallback_trends():
    """Diverse fallback topics covering ALL niches (NO AI BIAS)."""
    return [
        "shocking space discovery 2024",
        "bizarre animal behavior caught on camera",
        "hidden secrets of ancient pyramids",
        "most expensive things ever sold",
        "unexplained mysteries of the ocean",
        "craziest world records broken recently",
        "future of human space travel",
        "psychological tricks marketers use",
        "foods that are secretly dangerous",
        "abandoned places you can actually visit",
        "how billionaires spend their money",
        "deadly natural phenomena explained",
        "forgotten inventions that changed the world",
        "strangest things found in the desert",
        "cities that are sinking into the ocean"
    ]


def generate_viral_titles_with_llm(topic: str, language: str, count: int = 10):
    """Generate viral titles using Local LLM, strictly based on the provided topic."""
    print(f"\n🧠 Generating {count} viral titles in {language} for: '{topic}'...")
    
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        model_id = "HuggingFaceTB/SmolLM2-360M-Instruct"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print("   ⏳ Loading local LLM (one-time, ~15 seconds)...")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
        
        if language == 'persian':
            prompt = f"""You are a viral YouTube Shorts title expert. Generate exactly {count} short, click-worthy titles in PERSIAN (فارسی) about this EXACT topic: "{topic}"

RULES:
- Each title MUST be under 50 characters.
- Use numbers (۱, ۲, ۳...), power words, and questions.
- Make them shocking, curious, or urgent.
- DO NOT force "AI" into the title unless the topic is explicitly about AI.
- Return ONLY a JSON array of strings, nothing else.

Example: ["۵ راز باورنکردنی اقیانوس", "آیا این مکان واقعی است؟"]
JSON array:"""
        else:
            prompt = f"""You are a viral YouTube Shorts title expert. Generate exactly {count} short, click-worthy titles in ENGLISH about this EXACT topic: "{topic}"

RULES:
- Each title MUST be under 50 characters.
- Use numbers, power words, and questions.
- Make them shocking, curious, or urgent.
- DO NOT force "AI" into the title unless the topic is explicitly about AI.
- Return ONLY a JSON array of strings, nothing else.

Example: ["5 Shocking Ocean Secrets", "Is This Place Real?"]
JSON array:"""
        
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs, max_new_tokens=400, temperature=0.8, do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        titles = _extract_json_array(response)
        
    except Exception as e:
        print(f"   ⚠️ LLM generation failed ({e}). Using smart templates...")
        titles = _generate_template_titles(topic, language, count)
    
    # Clean and format
    final_titles = []
    seen = set()
    for t in titles:
        t = t.strip().strip('"').strip("'").strip('-').strip()
        if len(t) > 50:
            t = t[:47] + '...'
        if t and len(t) > 5 and t.lower() not in seen:
            seen.add(t.lower())
            final_titles.append(t)
        if len(final_titles) >= count:
            break
            
    return final_titles[:count] if final_titles else _generate_template_titles(topic, language, count)


def _extract_json_array(text: str):
    import re
    match = re.search(r'\[.*?\]', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    items = re.findall(r'"([^"]+)"', text)
    return items if items else [l.strip().strip('-').strip() for l in text.split('\n') if l.strip()]


def _generate_template_titles(topic: str, language: str, count: int):
    if language == 'persian':
        return [
            f"۵ حقیقت شوکه‌کننده درباره {topic[:25]}",
            f"راز پنهان {topic[:25]} فاش شد!",
            f"چرا همه درباره {topic[:25]} حرف می‌زنند؟",
            f"{topic[:25]}: چیزی که به شما نگفتند",
            f"۳ نکته عجیب درباره {topic[:25]}",
            f"آیا {topic[:25]} واقعیت دارد؟",
            f"ترسناک‌ترین حقیقت {topic[:25]}",
            f"{topic[:25]} در ۶۰ ثانیه",
            f"۷ راز باورنکردنی {topic[:25]}",
            f"آینده {topic[:25]} چگونه خواهد بود؟"
        ]
    else:
        return [
            f"5 Shocking Facts About {topic[:25]}",
            f"The Hidden Secret of {topic[:25]} Exposed!",
            f"Why Everyone is Talking About {topic[:25]}",
            f"{topic[:25]}: What They Didn't Tell You",
            f"3 Weird Things About {topic[:25]}",
            f"Is {topic[:25]} Actually Real?",
            f"The Scariest Truth About {topic[:25]}",
            f"{topic[:25]} Explained in 60 Seconds",
            f"7 Mind-Blowing Secrets of {topic[:25]}",
            f"What is the Future of {topic[:25]}?"
        ]


def main():
    print("=" * 70)
    print("🌍 COLAB SHORTS FACTORY - GLOBAL 24H TREND GENERATOR")
    print("=" * 70)
    
    # 1. Language
    print("\n🌐 Select Language / انتخاب زبان:")
    print("   [1] 🇬🇧 English")
    print("   [2] 🇮🇷 فارسی (Persian)")
    lang_choice = input("👉 Enter 1 or 2: ").strip()
    language = 'persian' if lang_choice == '2' else 'english'
    
    # 2. Fetch Trends
    trends = fetch_global_24h_trends()
    
    print("\n🔥 TOP GLOBAL TRENDS (Last 24 Hours):")
    for i, trend in enumerate(trends[:10], 1):
        print(f"   [{i:2d}] {trend}")
    print("   [ 0] ✏️  Enter a completely custom topic")
    
    # 3. Select Topic
    while True:
        try:
            choice = input(f"\n👉 Select a trend (0-{len(trends)}): ").strip()
            choice_num = int(choice)
            if choice_num == 0:
                topic = input("✏️ Enter your custom topic: ").strip()
                if topic: break
            elif 1 <= choice_num <= len(trends):
                topic = trends[choice_num - 1]
                print(f"✅ Selected: '{topic}'")
                break
            else:
                print(f"⚠️ Please enter 0-{len(trends)}.")
        except ValueError:
            print("⚠️ Please enter a valid number.")
    
    # 4. Generate Titles
    titles = generate_viral_titles_with_llm(topic, language, count=10)
    
    print("\n" + "=" * 70)
    print("🎯 SELECT A VIRAL TITLE (All under 50 characters):")
    print("=" * 70)
    for i, t in enumerate(titles, 1):
        print(f"   [{i:2d}] {t} ({len(t)} chars)")
    print("   [ 0] ✏️  Write your own title")
    
    # 5. Select Title
    while True:
        try:
            choice = input(f"\n👉 Select a title (0-{len(titles)}): ").strip()
            choice_num = int(choice)
            if choice_num == 0:
                final_title = input("✏️ Enter your custom title (max 50 chars): ").strip()[:50]
                if final_title: break
            elif 1 <= choice_num <= len(titles):
                final_title = titles[choice_num - 1]
                print(f"✅ Final Title: '{final_title}'")
                break
            else:
                print(f"⚠️ Please enter 0-{len(titles)}.")
        except ValueError:
            print("⚠️ Please enter a valid number.")
    
    # 6. Run Pipeline
    print("\n" + "=" * 70)
    print(f"🚀 Starting video generation for: '{final_title}'")
    print("=" * 70 + "\n")
    
    from app import run_pipeline
    import asyncio
    try:
        asyncio.run(run_pipeline(final_title))
    except Exception as e:
        os.system(f'{sys.executable} app.py "{final_title}"')

if __name__ == "__main__":
    main()        if t.lower() not in seen:
            seen.add(t.lower())
            unique_titles.append(t)
    
    return unique_titles[:count]


def _extract_keywords(topic: str):
    """Extract meaningful keywords from a topic string."""
    stop_words = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'can', 'to', 'of', 'in',
        'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'and',
        'but', 'or', 'not', 'so', 'yet', 'about', 'up', 'out', 'if',
        'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them',
        'we', 'our', 'you', 'your', 'he', 'she', 'his', 'her', 'my',
        'me', 'i', 'am', 'what', 'which', 'who', 'how', 'when', 'where'
    }
    words = topic.lower().replace(',', '').replace('.', '').replace('?', '').split()
    return [w for w in words if w not in stop_words and len(w) > 2][:4]


def _generate_english_titles(keywords, topic):
    """Generate viral English titles following 2026 standards."""
    kw = keywords[0] if keywords else 'AI'
    kw2 = keywords[1] if len(keywords) > 1 else 'future'
    
    templates = [
        f"5 {kw.title()} Facts That Shock You",
        f"{kw.title()} in 2026: What Changed?",
        f"Is {kw.title()} Replacing {kw2.title()}?",
        f"3 {kw.title()} Secrets Nobody Tells",
        f"{kw.title()}: The Truth Exposed",
        f"Why {kw.title()} Will Change Everything",
        f"{kw.title()} vs Humans: Who Wins?",
        f"Stop Ignoring {kw.title()} Now!",
        f"7 {kw.title()} Trends for 2026",
        f"{kw.title()}: 60-Second Explainer",
        f"Can {kw.title()} Save the World?",
        f"The Dark Side of {kw.title()}",
        f"{kw.title()} Just Got Scary Good",
        f"10 {kw.title()} Tools You Need",
        f"Is {kw.title()} Dangerous? Watch This",
    ]
    
    return templates


def _generate_persian_titles(keywords, topic):
    """Generate viral Persian titles following 2026 standards."""
    # Map common English keywords to Persian
    keyword_map = {
        'artificial': 'هوش مصنوعی', 'intelligence': 'هوش مصنوعی', 'ai': 'هوش مصنوعی',
        'quantum': 'کوانتوم', 'computing': 'رایانش', 'robot': 'ربات',
        'robotics': 'رباتیک', 'space': 'فضا', 'tourism': 'گردشگری',
        'climate': 'آب‌وهوا', 'change': 'تغییرات', 'health': 'سلامت',
        'healthcare': 'پزشکی', 'brain': 'مغز', 'computer': 'کامپیوتر',
        'interface': 'رابط', 'music': 'موسیقی', 'art': 'هنر',
        'cybersecurity': 'امنیت سایبری', 'surgery': 'جراحی',
        'education': 'آموزش', 'electric': 'الکتریکی', 'vehicles': 'خودرو',
        'metaverse': 'متاورس', 'virtual': 'مجازی', 'reality': 'واقعیت',
        'deepfake': 'دیپ‌فیک', 'detection': 'تشخیص', 'jobs': 'مشاغل',
        'careers': 'شغل‌ها', 'self': 'خودران', 'driving': 'خودران',
        'cars': 'خودروها', 'news': 'اخبار', 'breakthroughs': 'پیشرفت‌ها',
        'applications': 'کاربردها', 'diagnosis': 'تشخیص', 'updates': 'تحولات',
        'solutions': 'راه‌حل‌ها', 'advances': 'پیشرفت‌ها', 'personalized': 'شخصی‌سازی',
        'learning': 'یادگیری', 'future': 'آینده', 'threats': 'تهدیدات',
    }
    
    kw_fa = 'هوش مصنوعی'  # Default
    for kw in keywords:
        if kw.lower() in keyword_map:
            kw_fa = keyword_map[kw.lower()]
            break
    
    templates = [
        f"۵ راز باورنکردنی {kw_fa}",
        f"{kw_fa} در ۲۰۲۶: چه تغییر کرد؟",
        f"آیا {kw_fa} جایگزین انسان می‌شود؟",
        f"۳ حقیقت عجیب درباره {kw_fa}",
        f"{kw_fa}: حقیقتی که پنهان می‌کنند",
        f"چرا {kw_fa} همه‌چیز را عوض می‌کند؟",
        f"{kw_fa} در برابر انسان: کی برنده است؟",
        f"اگر {kw_fa} را نشناسید، ضرر کردید!",
        f"۷ ترند {kw_fa} در سال ۲۰۲۶",
        f"{kw_fa} در ۶۰ ثانیه: ساده و سریع",
        f"آیا {kw_fa} دنیا را نجات می‌دهد؟",
        f"نیمه تاریک {kw_fa} چیست؟",
        f"{kw_fa} ترسناک‌تر از همیشه شده!",
        f"۱۰ ابزار {kw_fa} که باید بشناسید",
        f"آیا {kw_fa} خطرناک است؟ ببینید!",
    ]
    
    return templates


def display_title_menu(titles):
    """Display numbered title menu and get user selection."""
    print("\n" + "=" * 60)
    print("🎯 SELECT A VIRAL TITLE FOR YOUR VIDEO")
    print("=" * 60)
    print("   (All titles are optimized for 2026: under 50 chars)\n")
    
    for i, title in enumerate(titles, 1):
        char_count = len(title)
        indicator = "✅" if char_count <= 45 else "⚠️"
        print(f"   {indicator} [{i:2d}] {title} ({char_count} chars)")
    
    print(f"\n   [ 0] ✏️  Enter your own custom title")
    print("=" * 60)
    
    while True:
        try:
            choice = input("\n👉 Enter your choice (0-10): ").strip()
            choice_num = int(choice)
            
            if choice_num == 0:
                custom = input("✏️ Enter your custom title (max 50 chars): ").strip()
                if custom:
                    return custom[:50]
                else:
                    print("⚠️ Title cannot be empty. Try again.")
                    continue
            elif 1 <= choice_num <= len(titles):
                selected = titles[choice_num - 1]
                print(f"\n✅ Selected: '{selected}'")
                return selected
            else:
                print(f"⚠️ Please enter a number between 0 and {len(titles)}.")
        except ValueError:
            print("⚠️ Please enter a valid number.")


def display_language_menu():
    """Display language selection menu."""
    print("\n" + "=" * 60)
    print("🌐 SELECT VIDEO LANGUAGE")
    print("=" * 60)
    print("   [1] 🇬🇧 English")
    print("   [2] 🇮🇷 فارسی (Persian)")
    print("=" * 60)
    
    while True:
        choice = input("\n👉 Enter your choice (1 or 2): ").strip()
        if choice == '1':
            print("✅ Language: English")
            return 'english'
        elif choice == '2':
            print("✅ Language: فارسی")
            return 'persian'
        else:
            print("⚠️ Please enter 1 or 2.")


def main():
    """Main interactive flow."""
    print("=" * 60)
    print("🎬 COLAB SHORTS FACTORY - VIRAL VIDEO GENERATOR")
    print("=" * 60)
    
    # Step 1: Choose mode
    print("\n📋 Choose generation mode:")
    print("   [1] 🔥 Auto-Generate from REAL Google Trends")
    print("   [2] ✏️  Enter Custom Topic")
    
    while True:
        mode = input("\n👉 Enter your choice (1 or 2): ").strip()
        if mode in ['1', '2']:
            break
        print("⚠️ Please enter 1 or 2.")
    
    # Step 2: Choose language
    language = display_language_menu()
    
    # Step 3: Get topic
    if mode == '1':
        trends = fetch_real_trends()
        print("\n📊 Top Trending Topics:")
        for i, trend in enumerate(trends[:10], 1):
            print(f"   [{i:2d}] {trend}")
        print(f"   [ 0] ✏️  Enter your own topic")
        
        while True:
            try:
                choice = input("\n👉 Select a trend (0-10): ").strip()
                choice_num = int(choice)
                if choice_num == 0:
                    topic = input("✏️ Enter your topic: ").strip()
                    if topic:
                        break
                elif 1 <= choice_num <= len(trends):
                    topic = trends[choice_num - 1]
                    print(f"✅ Selected trend: '{topic}'")
                    break
                else:
                    print(f"⚠️ Please enter 0-{len(trends)}.")
            except ValueError:
                print("⚠️ Please enter a valid number.")
    else:
        topic = input("\n✏️ Enter your video topic: ").strip()
        if not topic:
            topic = "artificial intelligence 2026"
            print(f"⚠️ Empty topic. Using default: '{topic}'")
    
    # Step 4: Generate 10 viral titles
    titles = generate_viral_titles(topic, language, count=10)
    
    # Step 5: User selects title
    selected_title = display_title_menu(titles)
    
    # Step 6: Run the pipeline
    print("\n" + "=" * 60)
    print(f"🎬 Starting video generation for:")
    print(f"   Title: '{selected_title}'")
    print(f"   Language: {language}")
    print("=" * 60 + "\n")
    
    # Import and run the main pipeline
    from app import run_pipeline
    import asyncio
    
    try:
        asyncio.run(run_pipeline(selected_title))
    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
        # Fallback: run via command line
        os.system(f'{sys.executable} app.py "{selected_title}"')


if __name__ == "__main__":
    main()
