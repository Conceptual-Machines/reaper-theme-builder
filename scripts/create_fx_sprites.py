#!/usr/bin/env python3
"""
Create FX sprite sheets from Figma assets.

FX files needed:
- track_fx_norm.png, track_fx_dis.png, track_fx_empty.png (FX text button)
- track_fxon_h.png, track_fxoff_h.png, track_fxempty_h.png (power icon horizontal)
- track_fxon_v.png, track_fxoff_v.png, track_fxempty_v.png (power icon vertical)
- Plus _ol overlay variants
- mcp_fx_norm.png, mcp_fx_dis.png, mcp_fx_empty.png (MCP FX text)
"""

from PIL import Image, ImageEnhance
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets" / "fx"
BUILD_DIR = PROJECT_ROOT / "build" / "DarkMinimal_unpacked"


def create_sprite(img, frame_size, brightness_factors=(1.0, 1.1, 1.2)):
    """
    Create a 3-frame horizontal sprite from single image.
    Maintains aspect ratio and centers in frame.
    """
    # Calculate scaling to fit in frame while maintaining aspect ratio
    scale_w = frame_size[0] / img.width
    scale_h = frame_size[1] / img.height
    scale = min(scale_w, scale_h) * 0.9  # 90% to add some padding
    
    new_w = int(img.width * scale)
    new_h = int(img.height * scale)
    
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Create centered frame
    frame = Image.new('RGBA', frame_size, (0, 0, 0, 0))
    x = (frame_size[0] - new_w) // 2
    y = (frame_size[1] - new_h) // 2
    frame.paste(resized, (x, y), resized)
    
    # Create 3 brightness variations
    states = []
    for bf in brightness_factors:
        if bf == 1.0:
            states.append(frame.copy())
        else:
            enhancer = ImageEnhance.Brightness(frame)
            states.append(enhancer.enhance(bf))
    
    # Combine into sprite sheet
    sprite_width = frame_size[0] * 3
    sprite = Image.new('RGBA', (sprite_width, frame_size[1]), (0, 0, 0, 0))
    
    for i, state in enumerate(states):
        sprite.paste(state, (i * frame_size[0], 0))
    
    return sprite


def save_with_dpi(img, base_path):
    """Save image at 1x, 1.5x, 2x DPI."""
    for folder, scale in [('', 1.0), ('150', 1.5), ('200', 2.0)]:
        if folder:
            out_dir = base_path.parent / folder
            out_dir.mkdir(exist_ok=True)
            out_path = out_dir / base_path.name
        else:
            out_path = base_path
        
        if scale != 1.0:
            new_size = (int(img.width * scale), int(img.height * scale))
            scaled = img.resize(new_size, Image.Resampling.LANCZOS)
            scaled.save(out_path)
        else:
            img.save(out_path)
    
    print(f"  ✓ {base_path.name}")


def process_fx_sprites():
    """Create all FX sprites from Figma assets."""
    
    # Load assets
    tcp_text_on = Image.open(ASSETS_DIR / "tcp_fx_text_on.png")
    text_off = Image.open(ASSETS_DIR / "fx_text_off.png")
    text_empty = Image.open(ASSETS_DIR / "fx_text_empty.png")
    
    tcp_power_on = Image.open(ASSETS_DIR / "tcp_fx_power_on.png")
    power_off = Image.open(ASSETS_DIR / "fx_power_off.png")
    power_empty = Image.open(ASSETS_DIR / "fx_power_empty.png")
    
    mcp_text_on = Image.open(ASSETS_DIR / "mcp_fx_text_on.png")
    mcp_power_on = Image.open(ASSETS_DIR / "mcp_fx_power_on.png")
    
    # TCP FX Text buttons (28x28 frames -> 84x28 sprite)
    print("\n=== TCP FX Text sprites ===")
    TCP_TEXT_SIZE = (28, 28)
    
    save_with_dpi(create_sprite(tcp_text_on, TCP_TEXT_SIZE), BUILD_DIR / "track_fx_norm.png")
    save_with_dpi(create_sprite(text_off, TCP_TEXT_SIZE), BUILD_DIR / "track_fx_dis.png")
    save_with_dpi(create_sprite(text_empty, TCP_TEXT_SIZE), BUILD_DIR / "track_fx_empty.png")
    save_with_dpi(create_sprite(tcp_text_on, TCP_TEXT_SIZE), BUILD_DIR / "track_fx_in_norm.png")
    save_with_dpi(create_sprite(text_empty, TCP_TEXT_SIZE), BUILD_DIR / "track_fx_in_empty.png")
    
    # TCP FX Text overlays (90x32 with empty space)
    TCP_OL_SIZE = (30, 32)
    for name, img in [("track_fx_norm_ol.png", tcp_text_on), 
                       ("track_fx_dis_ol.png", text_off),
                       ("track_fx_empty_ol.png", text_empty)]:
        sprite = create_sprite(img, TCP_OL_SIZE)
        final = Image.new('RGBA', (90, 32), (0, 0, 0, 0))
        final.paste(sprite, (0, 0))
        save_with_dpi(final, BUILD_DIR / name)
    
    # TCP Power icons horizontal (24x28 frames -> 72x28 sprite)
    print("\n=== TCP Power Icon sprites (horizontal) ===")
    TCP_POWER_SIZE = (24, 28)
    
    save_with_dpi(create_sprite(tcp_power_on, TCP_POWER_SIZE), BUILD_DIR / "track_fxon_h.png")
    save_with_dpi(create_sprite(power_off, TCP_POWER_SIZE), BUILD_DIR / "track_fxoff_h.png")
    save_with_dpi(create_sprite(power_empty, TCP_POWER_SIZE), BUILD_DIR / "track_fxempty_h.png")
    
    # TCP Power overlays horizontal (78x32)
    TCP_POWER_OL = (26, 32)
    for name, img in [("track_fxon_h_ol.png", tcp_power_on),
                       ("track_fxoff_h_ol.png", power_off),
                       ("track_fxempty_h_ol.png", power_empty)]:
        sprite = create_sprite(img, TCP_POWER_OL)
        final = Image.new('RGBA', (78, 32), (0, 0, 0, 0))
        final.paste(sprite, (0, 0))
        save_with_dpi(final, BUILD_DIR / name)
    
    # Vertical power indicators (thin strips)
    print("\n=== Vertical indicators ===")
    save_with_dpi(create_sprite(tcp_power_on, (3, 10)), BUILD_DIR / "track_fxon_v.png")
    save_with_dpi(create_sprite(power_off, (3, 10)), BUILD_DIR / "track_fxoff_v.png")
    save_with_dpi(create_sprite(power_empty, (3, 10)), BUILD_DIR / "track_fxempty_v.png")
    
    # Vertical overlays (62x20)
    for name, img in [("track_fxon_v_ol.png", tcp_power_on),
                       ("track_fxoff_v_ol.png", power_off),
                       ("track_fxempty_v_ol.png", power_empty)]:
        sprite = create_sprite(img, (21, 20))
        final = Image.new('RGBA', (62, 20), (0, 0, 0, 0))
        final.paste(sprite, (0, 0))
        save_with_dpi(final, BUILD_DIR / name)
    
    # MCP FX Text (slightly smaller)
    print("\n=== MCP FX Text sprites ===")
    MCP_TEXT_SIZE = (20, 20)
    
    save_with_dpi(create_sprite(mcp_text_on, MCP_TEXT_SIZE), BUILD_DIR / "mcp_fx_norm.png")
    save_with_dpi(create_sprite(text_off, MCP_TEXT_SIZE), BUILD_DIR / "mcp_fx_dis.png")
    save_with_dpi(create_sprite(text_empty, MCP_TEXT_SIZE), BUILD_DIR / "mcp_fx_empty.png")
    save_with_dpi(create_sprite(mcp_text_on, MCP_TEXT_SIZE), BUILD_DIR / "mcp_fx_in_norm.png")
    save_with_dpi(create_sprite(text_empty, MCP_TEXT_SIZE), BUILD_DIR / "mcp_fx_in_empty.png")


if __name__ == '__main__':
    print("=" * 50)
    print("FX Sprite Generator")
    print("=" * 50)
    
    process_fx_sprites()
    
    print("\n" + "=" * 50)
    print("Done!")
    print("=" * 50)
