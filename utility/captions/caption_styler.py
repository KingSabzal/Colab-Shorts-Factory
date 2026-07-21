"""
Caption Styler
==============
Applies visual styles to timed captions based on user configuration.
Supports 6 different caption styles: hormozi, card, neon, minimal, karaoke, comic.

This module is responsible for generating MoviePy TextClip objects with
appropriate styling based on the CAPTION_STYLE environment variable.
"""
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from utility.config import get_config, ConfigurationError


# ==========================================
# Style Presets
# ==========================================
STYLE_PRESETS = {
    'hormozi': {
        'fontsize': 100,
        'font': 'Arial-Bold',
        'color': 'yellow',
        'stroke_color': 'black',
        'stroke_width': 4,
        'position': 'bottom_center',
        'description': 'Bold, yellow/white, thick black outline (Highest engagement)'
    },
    'card': {
        'fontsize': 80,
        'font': 'Arial',
        'color': 'white',
        'stroke_color': 'black',
        'stroke_width': 2,
        'position': 'bottom_center',
        'description': 'White text on semi-transparent black background (Best readability)'
    },
    'neon': {
        'fontsize': 90,
        'font': 'Arial-Bold',
        'color': 'cyan',
        'stroke_color': 'magenta',
        'stroke_width': 3,
        'position': 'bottom_center',
        'description': 'Glowing cyan/magenta text (Gen-Z aesthetic)'
    },
    'minimal': {
        'fontsize': 70,
        'font': 'Helvetica',
        'color': 'white',
        'stroke_color': 'black',
        'stroke_width': 1,
        'position': 'bottom_center',
        'description': 'Clean white text, thin outline (Professional)'
    },
    'karaoke': {
        'fontsize': 95,
        'font': 'Arial-Bold',
        'color': 'yellow',
        'stroke_color': 'black',
        'stroke_width': 3,
        'position': 'bottom_center',
        'description': 'Highlights current word (High retention)'
    },
    'comic': {
        'fontsize': 85,
        'font': 'Comic-Sans-MS',
        'color': 'white',
        'stroke_color': 'black',
        'stroke_width': 4,
        'position': 'bottom_center',
        'description': 'Playful font with thick outline (Entertainment)'
    }
}

# ==========================================
# Fallback Fonts (in order of preference)
# ==========================================
FONT_FALLBACKS = [
    'Arial-Bold',
    'Arial',
    'DejaVu-Sans-Bold',
    'DejaVu-Sans',
    'Liberation-Sans-Bold',
    'Liberation-Sans',
    'Helvetica',
    'sans-serif'
]


def get_caption_clips(text: str, t1: float, t2: float, config):
    """
    Generates a MoviePy TextClip for a single caption word/segment.
    
    Args:
        text: The caption text to display.
        t1: Start time in seconds.
        t2: End time in seconds.
        config: Config instance with caption settings.
    
    Returns:
        MoviePy TextClip or CompositeVideoClip with styled caption.
    """
    # Get style from config
    style = config.get_caption_style()
    
    # Get style preset (fallback to hormozi if unknown)
    preset = STYLE_PRESETS.get(style, STYLE_PRESETS['hormozi'])
    
    # Override preset with user config (if specified)
    fontsize = config.get_caption_font_size() or preset['fontsize']
    font = config.get_caption_font_face() or preset['font']
    color = config.get_caption_font_color() or preset['color']
    stroke_color = config.get_caption_stroke_color() or preset['stroke_color']
    stroke_width = config.get_caption_stroke_width() or preset['stroke_width']
    position = config.get_caption_position() or preset['position']
    
    # Determine video dimensions based on orientation
    is_landscape = config.get_video_orientation()
    video_width = 1920 if is_landscape else 1080
    video_height = 1080 if is_landscape else 1920
    
    # Try to create TextClip with specified font, fallback if needed
    clip = _create_text_clip_with_fallback(
        text=text,
        fontsize=fontsize,
        font=font,
        color=color,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        video_width=video_width
    )
    
    # Set timing
    clip = clip.set_start(t1).set_end(t2)
    
    # Apply position based on style and config
    clip = _apply_position(clip, position, style, video_width, video_height)
    
    # Apply style-specific effects
    if style == 'card':
        clip = _apply_card_background(clip, video_width, video_height, position)
    
    return clip


def _create_text_clip_with_fallback(text: str, fontsize: int, font: str, 
                                     color: str, stroke_color: str, 
                                     stroke_width: int, video_width: int):
    """
    Create a TextClip with font fallback support.
    If the specified font is not available, tries fallback fonts.
    """
    # Try with specified font first
    fonts_to_try = [font] + [f for f in FONT_FALLBACKS if f != font]
    
    for font_name in fonts_to_try:
        try:
            clip = TextClip(
                text,
                fontsize=fontsize,
                font=font_name,
                color=color,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
                method='caption',
                size=(video_width - 100, None)  # Leave 50px margin on each side
            )
            # If we get here without error, font worked
            return clip
        except Exception as e:
            # Font not available, try next fallback
            continue
    
    # Last resort: create clip without font specification
    try:
        clip = TextClip(
            text,
            fontsize=fontsize,
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            method='caption',
            size=(video_width - 100, None)
        )
        return clip
    except Exception as e:
        raise ConfigurationError(f"Failed to create TextClip: {e}")


def _apply_position(clip, position: str, style: str, video_width: int, video_height: int):
    """
    Apply position to the caption clip based on style and configuration.
    """
    # Calculate vertical position with padding
    padding = 150  # Distance from bottom
    
    if position == 'bottom_center':
        clip = clip.set_position(('center', video_height - padding - clip.h))
    elif position == 'bottom':
        clip = clip.set_position(('center', video_height - padding - clip.h))
    elif position == 'bottom_left':
        clip = clip.set_position((50, video_height - padding - clip.h))
    elif position == 'bottom_right':
        clip = clip.set_position((video_width - clip.w - 50, video_height - padding - clip.h))
    elif position == 'center':
        clip = clip.set_position(('center', 'center'))
    elif position == 'top':
        clip = clip.set_position(('center', 100))
    else:
        # Default to bottom_center
        clip = clip.set_position(('center', video_height - padding - clip.h))
    
    return clip


def _apply_card_background(clip, video_width: int, video_height: int, position: str):
    """
    Apply semi-transparent black background for 'card' style.
    Creates a composite clip with background + text.
    """
    try:
        # Calculate background dimensions
        bg_width = clip.w + 40  # 20px padding on each side
        bg_height = clip.h + 20  # 10px padding on top/bottom
        
        # Create semi-transparent black background
        background = ColorClip(
            size=(bg_width, bg_height),
            color=(0, 0, 0)
        ).set_opacity(0.7)
        
        # Position background relative to text
        if position in ['bottom_center', 'bottom']:
            bg_x = (video_width - bg_width) // 2
            bg_y = video_height - 150 - clip.h - 10
        elif position == 'center':
            bg_x = (video_width - bg_width) // 2
            bg_y = (video_height - bg_height) // 2
        else:
            bg_x = (video_width - bg_width) // 2
            bg_y = video_height - 150 - clip.h - 10
        
        background = background.set_position((bg_x, bg_y))
        
        # Composite background and text
        composite = CompositeVideoClip([background, clip])
        return composite
        
    except Exception as e:
        # If card background fails, return original clip
        return clip


def get_caption_style_info(style: str = None):
    """
    Get information about available caption styles.
    
    Args:
        style: Specific style name (optional). If None, returns all styles.
    
    Returns:
        dict: Style information or all available styles.
    """
    if style:
        return STYLE_PRESETS.get(style, STYLE_PRESETS['hormozi'])
    return STYLE_PRESETS
