#!/usr/bin/env python3
"""
Copy ALL icons from Anti Theme to Default 7.0 base, except transport.
"""

import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ANTI_THEME = PROJECT_ROOT / "theme_source/AntiTheme/LCS_Flat-Anti-7_unpacked"
DEFAULT_THEME = PROJECT_ROOT / "theme_source/Default_7.0_unpacked"  # Copy to source, not build


def copy_icons():
    """Copy all PNG icons from Anti Theme to Default 7.0, except transport icons."""

    copied = 0

    # Copy from root directory
    for source_file in ANTI_THEME.glob("*.png"):
        # Skip transport icons (we have custom ones)
        if "transport_" in source_file.name:
            print(f"  ⊗ Skipped: {source_file.name} (custom transport)")
            continue

        dest_file = DEFAULT_THEME / source_file.name
        shutil.copy2(source_file, dest_file)
        print(f"  ✓ {source_file.name}")
        copied += 1

    # Copy from DPI folders (150, 200)
    for dpi_folder in ["150", "200"]:
        anti_dpi = ANTI_THEME / dpi_folder
        default_dpi = DEFAULT_THEME / dpi_folder

        if not anti_dpi.exists() or not default_dpi.exists():
            continue

        for source_file in anti_dpi.glob("*.png"):
            # Skip transport icons
            if "transport_" in source_file.name:
                continue

            dest_file = default_dpi / source_file.name
            shutil.copy2(source_file, dest_file)
            copied += 1

    print(f"\n✓ Copied {copied} icons from Anti Theme")


if __name__ == "__main__":
    print("=" * 50)
    print("Copying Anti Theme Icons")
    print("=" * 50)
    copy_icons()
    print("=" * 50)
