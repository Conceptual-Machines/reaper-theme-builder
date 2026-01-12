#!/usr/bin/env python3
"""
Update rtconfig.txt settings for the Default 7.0 DarkMinimal theme.
"""

import re
from pathlib import Path

RTCONFIG_PATH = Path(__file__).parent.parent / "build" / "Default_7.0_DarkMinimal_unpacked" / "rtconfig.txt"

# Transport bar settings
TRANSPORT_HEIGHT = 40  # Medium size (default was 36)
BUTTON_WIDTH = 36      # Square buttons
BUTTON_HEIGHT = 36     # Square buttons
BUTTON_SPACING = 2     # Tight spacing
BUTTON_Y_OFFSET = 2    # Center vertically: (40-36)/2 = 2
STATUS_WIDTH = 340     # Default was 450
SECTION_WIDTH = 380    # Width for buttons section


def update_rtconfig():
    """Update rtconfig.txt with new transport settings."""
    
    with open(RTCONFIG_PATH, 'r') as f:
        content = f.read()

    # Button size replacements (width height patterns)
    # Format: [x_offset y_offset width height]
    button_replacements = [
        # (pattern to find, replacement)
        (r"(set trans\.rew\s+.*Scale )\[0 0 \d+ \d+\]", f"\\1[0 0 {BUTTON_WIDTH} {BUTTON_HEIGHT}]"),
        (r"(set trans\.fwd\s+.*Scale )\[\d+ 0 \d+ \d+\]", f"\\1[{BUTTON_SPACING} 0 {BUTTON_WIDTH} {BUTTON_HEIGHT}]"),
        (r"(set trans\.rec\s+.*Scale )\[\d+ 0 \d+ \d+\]", f"\\1[{BUTTON_SPACING} 0 {BUTTON_WIDTH} {BUTTON_HEIGHT}]"),
        (r"(set trans\.play\s+.*Scale )\[-?\d+ 0 \d+ \d+\]", f"\\1[{BUTTON_SPACING} 0 {BUTTON_WIDTH} {BUTTON_HEIGHT}]"),
        (r"(set trans\.repeat\s+.*Scale )\[-?\d+ 0 \d+ \d+\]", f"\\1[{BUTTON_SPACING} 0 {BUTTON_WIDTH} {BUTTON_HEIGHT}]"),
        (r"(set trans\.stop\s+.*Scale )\[\d+ 0 \d+ \d+\]", f"\\1[{BUTTON_SPACING} 0 {BUTTON_WIDTH} {BUTTON_HEIGHT}]"),
        (r"(set trans\.pause\s+.*Scale )\[\d+ 0 \d+ \d+\]", f"\\1[{BUTTON_SPACING} 0 {BUTTON_WIDTH} {BUTTON_HEIGHT}]"),
    ]
    
    for pattern, replacement in button_replacements:
        content = re.sub(pattern, replacement, content)
    
    # Update sectionButtons: [transMargin y_offset width height] - center vertically
    content = re.sub(
        r"(set trans\.custom\.sectionButtons\s+\+ \* Scale )\[transMargin \d+ \d+ \d+\]",
        f"\\1[transMargin {BUTTON_Y_OFFSET} {SECTION_WIDTH} {BUTTON_HEIGHT}]",
        content
    )
    
    # Update status width parameter
    content = re.sub(
        r"(define_parameter transStatusWidth\s+'Status Width' )\d+",
        f"\\g<1>{STATUS_WIDTH}",
        content
    )
    
    # Update transport heights (36 -> TRANSPORT_HEIGHT)
    # trans.size, trans.size.dockedheight, etc.
    content = re.sub(
        r"(set trans\.size\s+\* Scale )\[1000 \d+\]",
        f"\\1[1000 {TRANSPORT_HEIGHT}]",
        content
    )
    content = re.sub(
        r"(set trans\.size\.dockedheight\s+\* Scale )\[\d+\]",
        f"\\1[{TRANSPORT_HEIGHT}]",
        content
    )
    
    # Update sectionLeft height (used as reference)
    content = re.sub(
        r"(set trans\.custom\.sectionLeft\s+\* Scale )\[0 0 1000 \d+\]",
        f"\\1[0 0 1000 {TRANSPORT_HEIGHT}]",
        content
    )
    
    # Update status section height - replace all 36 with TRANSPORT_HEIGHT in status lines
    # Pattern: [transMargin 0 transStatusWidth{0} 36] -> [transMargin 0 transStatusWidth{0} 48]
    content = re.sub(
        r"(\[transMargin 0 transStatusWidth\{0\}) 36\]",
        f"\\1 {TRANSPORT_HEIGHT}]",
        content
    )
    # Pattern: [0 36 transStatusWidth{0} 36] -> [0 6 transStatusWidth{0} 36] (y-offset 6 to center 36 in 48)
    content = re.sub(
        r"\[0 36 transStatusWidth\{0\} 36\]",
        f"[0 6 transStatusWidth{{0}} 36]",
        content
    )
    # Update minmax height
    content = re.sub(
        r"(set trans\.size\.minmax\s+\* Scale \+ \[100) 36 (2000) 144\]",
        f"\\1 {TRANSPORT_HEIGHT} \\2 {TRANSPORT_HEIGHT * 3}]",
        content
    )
    
    # Update right sections (BPM, Sig, Sel) - height from 36 to TRANSPORT_HEIGHT
    # Pattern: transFollow trans.custom.sectionBpm 60 36 -> 60 48
    content = re.sub(r"(transFollow trans\.custom\.sectionBpm\s+\d+) 36", f"\\1 {TRANSPORT_HEIGHT}", content)
    content = re.sub(r"(transFollow trans\.custom\.sectionSig\s+\d+) 36", f"\\1 {TRANSPORT_HEIGHT}", content)
    content = re.sub(r"(transFollow trans\.custom\.sectionSel\s+transSelectionWidth\{0\}) 36", f"\\1 {TRANSPORT_HEIGHT}", content)
    
    # Update previous reference for right sections
    content = re.sub(r"(set previous\s+\+ \[w trans\.custom\.sectionRight\] \* Scale \[0 0 0) 36\]", f"\\1 {TRANSPORT_HEIGHT}]", content)
    
    # Update the conditional y-offset for right section
    content = re.sub(r"(\[0 36\] \[0 transMargin)", f"[0 {TRANSPORT_HEIGHT}] [0 transMargin", content)
    
    # Update transport status background color - lighter (51,51,51 -> 70,70,70)
    content = re.sub(
        r"(\[0 0 0 0) 51 51 51 (255\])",
        r"\1 70 70 70 \2",
        content
    )
    
    with open(RTCONFIG_PATH, 'w') as f:
        f.write(content)
    
    print(f"✓ Updated rtconfig.txt")
    print(f"  Transport height: {TRANSPORT_HEIGHT}px")
    print(f"  Button size: {BUTTON_WIDTH}x{BUTTON_HEIGHT}px")
    print(f"  Button spacing: {BUTTON_SPACING}px")
    print(f"  Status width: {STATUS_WIDTH}px")


if __name__ == "__main__":
    update_rtconfig()
