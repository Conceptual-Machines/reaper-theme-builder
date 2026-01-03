#!/usr/bin/env python3
"""
DarkMinimal Theme Builder
Creates zip and deploys to REAPER ColorThemes folders.
"""

import os
import shutil
from pathlib import Path
import zipfile

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
BUILD_DIR = PROJECT_ROOT / "build" / "DarkMinimal_unpacked"
THEME_FILE = PROJECT_ROOT / "build" / "DarkMinimal_unpacked.ReaperTheme"
OUTPUT_ZIP = PROJECT_ROOT / "DarkMinimal.ReaperThemeZip"

# Deploy to BOTH portable and system REAPER
DEPLOY_DIRS = [
    Path("/Users/Luca_Romagnoli/Code/personal/ReaScript/reaper-portable/ColorThemes"),
    Path.home() / "Library/Application Support/REAPER/ColorThemes",
]


def create_zip():
    """Create the theme zip file."""
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
    
    print(f"Created: {OUTPUT_ZIP}")


def deploy():
    """Copy zip to REAPER ColorThemes folders (portable + system)."""
    for deploy_dir in DEPLOY_DIRS:
        if deploy_dir.exists():
            dest = deploy_dir / OUTPUT_ZIP.name
            shutil.copy2(OUTPUT_ZIP, dest)
            print(f"  ✓ {dest}")
        else:
            print(f"  ⚠ Not found: {deploy_dir}")


def main():
    print("=" * 50)
    print("DarkMinimal Theme Builder")
    print("=" * 50)
    
    print("\n[1/2] Creating zip...")
    create_zip()
    
    print("\n[2/2] Deploying...")
    deploy()
    
    print("\n" + "=" * 50)
    print("Done! Reload theme in REAPER.")
    print("=" * 50)


if __name__ == "__main__":
    main()
