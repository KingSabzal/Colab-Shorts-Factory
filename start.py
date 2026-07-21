"""
Colab Shorts Factory - Interactive Starter
==========================================
Fetches REAL Google Trends, generates 10 viral titles,
and lets the user choose language and title.

2026 Viral Title Standards:
- Max 50 characters (optimal for Shorts/TikTok/Reels)
- Use numbers, power words, questions
- No clickbait that misleads
"""
import os
import sys
import json

# Ensure we're in the project directory
project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

from utility.config import get_config


def fetch_real_trends():
    """
    Fetch REAL trending topics from Google Trends using pytrends.
    Falls back to curated 2026 topics if pytrends fails.
    """
    print("\n🔍 Fetching REAL Google Trends...")
    
    try:
        from pytrends.request import TrendReq
        
        # Connect to Google Trends
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
        
        # Get trending searches globally
        trending_df = pytrends.trending_searches(pn='united_states')
        
        if not trending_df.empty:
            # Get top 15 real trends
            trends = trending_df[0].head(15).tolist()
            print(f"   ✅ Found {len(trends)} real Google Trends!")
            for i, trend in enumerate(trends[:5], 1):
                print(f"      {i}. {trend}")
            return trends
        else:
            print("   ⚠️ No trends found from Google. Using curated topics...")
            return _get_curated_trends()
            
    except Exception as e:
        print(f"   ⚠️ Google Trends API error: {e}")
        print("   🔄 Using curated 2026 trending topics...")
        return _get_curated_trends()


def _get_curated_trends():
    """
    Curated list of 2026 trending topics across tech, science, health, finance.
    These are updated based on real-world events and search patterns.
    """
    return [
        "artificial intelligence breakthroughs 2026",
        "quantum computing real world applications",
        "AI replacing jobs which careers are safe",
        "self driving cars latest news",
        "AI in healthcare diagnosis",
        "space tourism 2026 updates",
        "climate change AI solutions",
        "brain computer interface Neuralink",
        "AI generated music and art",
        "cybersecurity threats 2026",
        "robotics surgery advances",
        "AI education personalized learning",
        "electric vehicles future",
        "metaverse virtual reality 2026",
        "AI deepfake detection"
    ]


def generate_viral_titles(topic: str, language: str, count: int = 10):
    """
    Generate 10 short, viral, click-worthy titles based on 2026 standards.
    
    Rules:
    - Max 50 characters per title
    - Use numbers, power words, questions
    - Match the selected language (Persian or English)
    """
    print(f"\n🧠 Generating {count} viral titles in {language}...")
    print(f"   📌 Topic: '{topic}'")
    
    # Extract key words from topic
    keywords = _extract_keywords(topic)
    
    if language == 'persian':
        titles = _generate_persian_titles(keywords, topic)
    else:
        titles = _generate_english_titles(keywords, topic)
    
    # Ensure all titles are under 50 characters
    titles = [t[:47] + '...' if len(t) > 50 else t for t in titles]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_titles = []
    for t in titles:
        if t.lower() not in seen:
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
