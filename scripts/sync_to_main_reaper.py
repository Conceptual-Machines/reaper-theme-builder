#!/usr/bin/env python3
"""
Sync theme and customizations from portable to main REAPER.
"""

import shutil
from pathlib import Path

# Source: portable REAPER
PORTABLE = Path.home() / "Dropbox/Code/Projects/ReaScript/reaper-portable"

# Destination: main REAPER
MAIN = Path.home() / "Library/Application Support/REAPER"

def sync_file(src, dst, description):
    """Sync a single file"""
    try:
        shutil.copy2(src, dst)
        print(f"✓ {description}")
        return True
    except Exception as e:
        print(f"✗ {description}: {e}")
        return False

def sync_directory(src, dst, description):
    """Sync a directory"""
    try:
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f"✓ {description}")
        return True
    except Exception as e:
        print(f"✗ {description}: {e}")
        return False

def sync_to_main():
    """Sync portable REAPER customizations to main installation"""

    print("=" * 50)
    print("Syncing to Main REAPER")
    print("=" * 50)

    syncs = [
        # Keyboard shortcuts
        (PORTABLE / "reaper-kb.ini", MAIN / "reaper-kb.ini",
         "Keyboard shortcuts (reaper-kb.ini)"),

        # Mouse modifiers
        (PORTABLE / "reaper-mouse.ini", MAIN / "reaper-mouse.ini",
         "Mouse modifiers (reaper-mouse.ini)"),
    ]

    # Sync files
    for src, dst, desc in syncs:
        if src.exists():
            sync_file(src, dst, desc)
        else:
            print(f"⊘ {desc}: source not found")

    # Sync toolbar icons
    src_icons = PORTABLE / "Data/toolbar_icons"
    dst_icons = MAIN / "Data/toolbar_icons"
    if src_icons.exists():
        sync_directory(src_icons, dst_icons, "Toolbar icons")

    print("=" * 50)
    print("Sync complete!")
    print()
    print("Note: Theme is already deployed by build_theme.py")
    print("Note: reaper.ini settings must be manually merged")
    print()

if __name__ == "__main__":
    sync_to_main()
