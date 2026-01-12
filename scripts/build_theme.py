#!/usr/bin/env python3
"""
Default 7.0 DarkMinimal Theme Builder
Creates zip and deploys to REAPER ColorThemes folders.
"""

import os
import sys
import shutil
from pathlib import Path
import zipfile

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
BUILD_DIR = PROJECT_ROOT / "build" / "Default_7.0_DarkMinimal_unpacked"
THEME_FILE = PROJECT_ROOT / "build" / "Default_7.0_DarkMinimal_unpacked.ReaperTheme"
OUTPUT_ZIP = PROJECT_ROOT / "Default_7.0_DarkMinimal.ReaperThemeZip"

# Load deployment configuration
# Users should copy deploy_config.example.py to deploy_config.py and customize
try:
    # Add project root to path to import deploy_config
    sys.path.insert(0, str(PROJECT_ROOT))
    from deploy_config import DEPLOY_DIRS
except ImportError:
    # No deploy_config.py found - skip deployment
    DEPLOY_DIRS = []


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
                arc_name = f"Default_7.0_DarkMinimal_unpacked/{file_path.relative_to(BUILD_DIR)}"
                zf.write(file_path, arc_name)
    
    print(f"Created: {OUTPUT_ZIP}")


def deploy():
    """Copy zip to REAPER ColorThemes folders (portable + system)."""
    if not DEPLOY_DIRS:
        print("  ⚠ No deployment targets configured.")
        print("  → Copy 'deploy_config.example.py' to 'deploy_config.py' and customize paths.")
        return

    deployed_count = 0
    for deploy_dir in DEPLOY_DIRS:
        if deploy_dir.exists():
            dest = deploy_dir / OUTPUT_ZIP.name
            shutil.copy2(OUTPUT_ZIP, dest)
            print(f"  ✓ {dest}")
            deployed_count += 1
        else:
            print(f"  ⚠ Not found: {deploy_dir}")

    if deployed_count == 0:
        print("  ⚠ No valid deployment targets found. Check paths in deploy_config.py")


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
