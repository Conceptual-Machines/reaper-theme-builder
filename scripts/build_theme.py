#!/usr/bin/env python3
"""
DarkMinimal Theme Builder
Copies source assets to build folder with correct REAPER naming.
"""

import os
import shutil
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
BUILD_DIR = PROJECT_ROOT / "build" / "DarkMinimal_unpacked"
THEME_FILE = PROJECT_ROOT / "build" / "DarkMinimal.ReaperTheme"
OUTPUT_ZIP = PROJECT_ROOT / "DarkMinimal.ReaperThemeZip"
DEPLOY_DIR = Path("/Users/Luca_Romagnoli/Code/personal/ReaScript/reaper-portable/ColorThemes")

# Transport image mapping: source -> [list of REAPER names]
TRANSPORT_MAPPING = {
    "play_off.png": ["transport_play.png", "transport_play_ol.png", "transport_play_sync.png", "transport_play_sync_ol.png"],
    "play_on.png": ["transport_play_on.png", "transport_play_sync_on.png"],
    "stop_off.png": ["transport_stop.png"],
    "stop_on.png": [],  # No on state for stop in default theme
    "pause_off.png": ["transport_pause.png"],
    "pause_on.png": ["transport_pause_on.png"],
    "record_off.png": ["transport_record.png", "transport_record_ol.png", "transport_record_item.png", "transport_record_item_ol.png", "transport_record_loop.png", "transport_record_loop_ol.png"],
    "record_on.png": ["transport_record_on.png", "transport_record_item_on.png", "transport_record_loop_on.png"],
    "rewind_off.png": ["transport_previous.png"],
    "rewind_on.png": ["transport_previous_on.png"],
    "forward_off.png": ["transport_next.png"],
    "forward_on.png": ["transport_next_on.png"],
    "prev_off.png": ["transport_home.png"],
    "prev_on.png": [],
    "next_off.png": ["transport_end.png"],
    "next_on.png": [],
    "loop_off.png": ["transport_repeat_off.png", "transport_repeat_ol.png"],
    "loop_on.png": ["transport_repeat_on.png"],
}

# DPI scale folders
DPI_FOLDERS = ["", "150", "200"]


def copy_transport_images():
    """Copy and rename transport images to build folder."""
    src_transport = SRC_DIR / "transport"
    
    if not src_transport.exists():
        print(f"Warning: {src_transport} not found")
        return
    
    for src_name, dest_names in TRANSPORT_MAPPING.items():
        src_file = src_transport / src_name
        
        if not src_file.exists():
            print(f"Warning: {src_file} not found")
            continue
        
        for dest_name in dest_names:
            for dpi in DPI_FOLDERS:
                if dpi:
                    dest_dir = BUILD_DIR / dpi
                else:
                    dest_dir = BUILD_DIR
                
                dest_file = dest_dir / dest_name
                
                if dest_dir.exists():
                    shutil.copy2(src_file, dest_file)
                    print(f"  {src_name} → {dpi + '/' if dpi else ''}{dest_name}")


def create_zip():
    """Create the theme zip file."""
    import zipfile
    
    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()
    
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add theme file
        zf.write(THEME_FILE, THEME_FILE.name)
        
        # Add all files from unpacked folder
        for root, dirs, files in os.walk(BUILD_DIR):
            for file in files:
                file_path = Path(root) / file
                arc_name = f"DarkMinimal_unpacked/{file_path.relative_to(BUILD_DIR)}"
                zf.write(file_path, arc_name)
    
    print(f"\nCreated: {OUTPUT_ZIP}")


def deploy():
    """Copy zip to REAPER ColorThemes folder."""
    if DEPLOY_DIR.exists():
        dest = DEPLOY_DIR / OUTPUT_ZIP.name
        shutil.copy2(OUTPUT_ZIP, dest)
        print(f"Deployed to: {dest}")
    else:
        print(f"Warning: Deploy directory not found: {DEPLOY_DIR}")


def main():
    print("=" * 50)
    print("DarkMinimal Theme Builder")
    print("=" * 50)
    
    # Skip transport images - handled by create_sprites.py
    # print("\n[1/3] Copying transport images...")
    # copy_transport_images()
    
    print("\n[1/2] Creating zip...")
    create_zip()
    
    print("\n[2/2] Deploying...")
    deploy()
    
    print("\n" + "=" * 50)
    print("Done! Reload theme in REAPER.")
    print("=" * 50)


if __name__ == "__main__":
    main()

