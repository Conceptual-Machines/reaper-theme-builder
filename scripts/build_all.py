#!/usr/bin/env python3
"""
Master build script for DarkMinimal theme.
Runs all build steps in the correct order.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def run_script(script_name, description):
    """Run a Python script and check for errors."""
    script_path = PROJECT_ROOT / script_name
    
    if not script_path.exists():
        print(f"  ⚠ Skipping {script_name} (not found)")
        return True
    
    print(f"\n{'─' * 50}")
    print(f"▶ {description}")
    print(f"{'─' * 50}")
    
    result = subprocess.run([sys.executable, str(script_path)], cwd=PROJECT_ROOT)
    
    if result.returncode != 0:
        print(f"  ✗ {script_name} failed!")
        return False
    
    return True


def main():
    print("=" * 50)
    print("🎨 DarkMinimal Theme - Full Build")
    print("=" * 50)
    
    steps = [
        ("scripts/update_rtconfig.py", "Updating rtconfig.txt settings"),
        ("scripts/create_sprites.py", "Creating transport icon sprites"),
        ("scripts/create_track_sprites.py", "Creating track button sprites"),
        ("scripts/build_theme.py", "Building and deploying theme"),
    ]
    
    for script, desc in steps:
        if not run_script(script, desc):
            print("\n✗ Build failed!")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✓ Build complete! Reload theme in REAPER.")
    print("=" * 50)


if __name__ == "__main__":
    main()

