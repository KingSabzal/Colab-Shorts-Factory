import os
import platform
from moviepy.editor import TextClip, ColorClip

# Font mapping for each 2026 caption style
# Each style has its own signature font as per viral video research
FONT_MAP = {
    'hormozi': ['Impact', 'Arial-Black', 'Arial-Bold'],
    'card': ['Helvetica', 'Arial', 'Verdana'],
    'neon': ['Arial-Bold', 'Helvetica-Bold', 'Impact'],
    'minimal': ['Helvetica', 'Arial', 'Calibri'],
    'karaoke': ['Impact', 'Arial-Black', 'Arial-Bold'],
    'comic': ['Comic Sans MS', 'Comic-Sans-MS', 'Chalkboard', 'Arial']
}

def get_available_font(preferred_fonts):
    """
    Tries each font in the list and returns the first one that works on the current system.
    This ensures cross-platform compatibility (Windows, Linux, Mac).
    """
    for font in preferred_fonts:
        try:
            # Test if the font is available by creating a small TextClip
            test_clip = TextClip(txt="test", font=font, fontsize=10, color='white')
            test_clip.close()
            return font
        except Exception:
            continue
    # Ultimate fallback
    return 'Arial-Bold'

def get_caption_clips(text, t1, t2, config):
    """
    Generates MoviePy clips for captions based on 2026 trending styles.
    Each style uses its own signature font, color scheme, and visual treatment.
    """
    style = config.get_caption_style()
    base_color = config.get_caption_font_color()
    stroke_width = config.get_caption_stroke_width()
    stroke_color = config.get_caption_stroke_color()
    position = config.get_caption_position()
    
    # Smart font selection:
    # If user customized CAPTION_FONT_FACE in .env (not default 'Arial-Bold'), use their font
    # Otherwise, use the signature font for this style from FONT_MAP
    user_font = config.get_caption_font_face()
    if user_font != 'Arial-Bold':
        # User override: use their custom font
        preferred_fonts = [user_font]
    else:
        # Use signature font for this style
        preferred_fonts = FONT_MAP.get(style, ['Arial-Bold'])
    
    font_face = get_available_font(preferred_fonts)
    
    # Position mapping for 1080p video
    pos_map = {
        'bottom_center': ('center', 900),
        'bottom_left': ('left', 900),
        'bottom_right': ('right', 900),
        'top': ('center', 150),
        'center': ('center', 540),
        'bottom': ('center', 950)
    }
    pos = pos_map.get(position, ('center', 900))
    clips = []

    # ==========================================
    # 2026 TRENDING CAPTION STYLES
    # Each style has its own font, color, and visual treatment
    # ==========================================
    
    if style == 'hormozi':
        # Signature: Impact font, yellow/white, thick black outline
        # Inspired by Alex Hormozi's viral shorts style
        font_size = config.get_caption_font_size()
        color = 'yellow' if base_color == 'yellow' else 'white'
        sw = max(stroke_width, 5)
        txt_clip = TextClip(txt=text, font=font_face, fontsize=font_size, color=color, 
                            stroke_width=sw, stroke_color='black', method='label')
        txt_clip = txt_clip.set_start(t1).set_end(t2).set_position(pos)
        clips.append(txt_clip)

    elif style == 'card':
        # Signature: Helvetica font, white text on semi-transparent black card
        # Best readability on any background
        font_size = config.get_caption_font_size()
        txt_clip = TextClip(txt=text, font=font_face, fontsize=font_size, color='white', 
                            stroke_width=0, stroke_color='transparent', method='label')
        txt_clip = txt_clip.set_start(t1).set_end(t2).set_position(pos)
        
        w, h = txt_clip.size
        padding = 15
        bg_clip = ColorClip(size=(int(w + padding*2), int(h + padding)), color=(0, 0, 0))
        bg_clip = bg_clip.set_start(t1).set_end(t2).set_opacity(0.6).set_position((pos[0], pos[1] - 5))
        clips.append(bg_clip)
        clips.append(txt_clip)

    elif style == 'neon':
        # Signature: Bold font with glowing neon effect (cyan/magenta)
        # Gen-Z aesthetic, high visual impact
        font_size = config.get_caption_font_size()
        neon_colors = ['cyan', 'magenta', 'green', 'blue', 'yellow']
        color = base_color if base_color in neon_colors else 'cyan'
        # Simulate glow with thick white stroke + colored text
        txt_clip = TextClip(txt=text, font=font_face, fontsize=font_size, color=color, 
                            stroke_width=3, stroke_color='white', method='label')
        txt_clip = txt_clip.set_start(t1).set_end(t2).set_position(pos)
        clips.append(txt_clip)

    elif style == 'minimal':
        # Signature: Helvetica font, clean white, thin outline
        # Professional, no distraction
        font_size = config.get_caption_font_size()
        txt_clip = TextClip(txt=text, font=font_face, fontsize=font_size, color='white', 
                            stroke_width=2, stroke_color='black', method='label')
        txt_clip = txt_clip.set_start(t1).set_end(t2).set_position(pos)
        clips.append(txt_clip)

    elif style == 'karaoke':
        # Signature: Impact font, highlights current word in yellow/green
        # High retention, keeps viewer focused
        font_size = config.get_caption_font_size()
        color = 'yellow' if base_color == 'yellow' else 'green'
        txt_clip = TextClip(txt=text, font=font_face, fontsize=font_size, color=color, 
                            stroke_width=4, stroke_color='black', method='label')
        txt_clip = txt_clip.set_start(t1).set_end(t2).set_position(pos)
        clips.append(txt_clip)

    elif style == 'comic':
        # Signature: Comic Sans font, playful and friendly
        # Entertainment, meme content, casual tone
        font_size = int(config.get_caption_font_size() * 1.1)
        txt_clip = TextClip(txt=text, font=font_face, fontsize=font_size, color='white', 
                            stroke_width=4, stroke_color='black', method='label')
        txt_clip = txt_clip.set_start(t1).set_end(t2).set_position(pos)
        clips.append(txt_clip)

    else:
        # Default fallback: use configured font
        font_size = config.get_caption_font_size()
        txt_clip = TextClip(txt=text, font=font_face, fontsize=font_size, color=base_color, 
                            stroke_width=stroke_width, stroke_color=stroke_color, method='label')
        txt_clip = txt_clip.set_start(t1).set_end(t2).set_position(pos)
        clips.append(txt_clip)

    return clips