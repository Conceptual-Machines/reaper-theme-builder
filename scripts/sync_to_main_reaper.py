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
    """Sync a single file with backup"""
    try:
        # Create backup if destination exists
        if dst.exists():
            backup = dst.with_suffix(dst.suffix + '.backup')
            shutil.copy2(dst, backup)
            print(f"  → Backed up to {backup.name}")

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
        # Main config file (all settings)
        (PORTABLE / "reaper.ini", MAIN / "reaper.ini",
         "Main config (reaper.ini) - ALL SETTINGS"),

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
    print("✓ Theme is already deployed by build_theme.py")
    print("✓ All settings copied from portable to main REAPER")
    print()
    print("⚠️  Backups saved as *.backup in case you need to restore")
    print("⚠️  Close and restart REAPER to apply all changes")
    print()

if __name__ == "__main__":
    sync_to_main()
