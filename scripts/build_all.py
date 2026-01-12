#!/usr/bin/env python3
"""
Master build script for DarkMinimal theme.
Runs all build steps in the correct order.
Can be run locally or in CI.
"""

import subprocess
import sys
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
THEME_SOURCE = PROJECT_ROOT / "theme_source"
BUILD_DIR = PROJECT_ROOT / "build"


def check_dependencies():
    """Verify required dependencies are installed."""
    try:
        from PIL import Image
        print("  ✓ Pillow installed")
        return True
    except ImportError:
        print("  ✗ Pillow not installed. Run: pip install -r requirements.txt")
        return False


def check_assets():
    """Verify required assets exist."""
    required_assets = [
        PROJECT_ROOT / "assets" / "transport" / "play_off.png",
        PROJECT_ROOT / "assets" / "transport" / "play_on.png",
        # FX assets are now sourced from LCS theme (no custom assets needed)
    ]
    
    missing = [a for a in required_assets if not a.exists()]
    if missing:
        print(f"  ✗ Missing assets:")
        for a in missing:
            print(f"      - {a.relative_to(PROJECT_ROOT)}")
        return False
    
    print("  ✓ Assets present")
    return True


def setup_build_directory():
    """Setup build directory from base theme."""

    # The unpacked theme folder should be checked into the repo
    theme_folder = THEME_SOURCE / "Default_7.0_unpacked"
    theme_file = THEME_SOURCE / "Default_7.0_unpacked.ReaperTheme"

    if not theme_folder.exists():
        print(f"  ✗ Base theme folder not found: {theme_folder}")
        print("    The Default 7.0 theme source files should be in the theme_source directory.")
        return False

    # Setup build directory
    build_unpacked = BUILD_DIR / "DarkMinimal_unpacked"
    build_theme = BUILD_DIR / "DarkMinimal_unpacked.ReaperTheme"

    if not build_unpacked.exists():
        print("  Copying base theme to build directory...")
        BUILD_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copytree(theme_folder, build_unpacked)
        shutil.copy2(theme_file, build_theme)

    print("  ✓ Build directory ready")
    return True


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
    
    # Pre-flight checks
    print("\n[1/3] Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("\n[2/3] Checking assets...")
    if not check_assets():
        sys.exit(1)
    
    print("\n[3/3] Setting up build directory...")
    if not setup_build_directory():
        sys.exit(1)
    
    # Build steps
    steps = [
        ("scripts/update_rtconfig.py", "Updating rtconfig.txt transport settings"),
        ("scripts/apply_colors.py", "Applying color palette"),
        ("scripts/create_transport_sprites.py", "Creating transport icon sprites"),
        ("scripts/create_fx_sprites.py", "Creating FX button sprites"),
        ("scripts/build_theme.py", "Building and deploying theme"),
    ]
    
    for script, desc in steps:
        if not run_script(script, desc):
            print("\n✗ Build failed!")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✓ Build complete!")
    print(f"  Output: {PROJECT_ROOT / 'DarkMinimal.ReaperThemeZip'}")
    print("=" * 50)


if __name__ == "__main__":
    main()
