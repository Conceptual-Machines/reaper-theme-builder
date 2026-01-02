#!/usr/bin/env python3
"""
Update rtconfig.txt settings for the DarkMinimal theme.
"""

import re
from pathlib import Path

RTCONFIG_PATH = Path(__file__).parent.parent / "build" / "DarkMinimal_unpacked" / "rtconfig.txt"

# Transport bar settings
TRANSPORT_HEIGHT = 48  # Default was 36
BUTTON_WIDTH = 48      # Default was 28-32  
BUTTON_HEIGHT = 42     # Default was 30
BUTTON_SPACING = 4     # Extra spacing between buttons
STATUS_WIDTH = 350     # Default was 450
SECTION_WIDTH = 400    # Width for buttons section


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
    
    # Update sectionButtons: [transMargin y_offset width height]
    content = re.sub(
        r"(set trans\.custom\.sectionButtons\s+\+ \* Scale )\[transMargin \d+ \d+ \d+\]",
        f"\\1[transMargin 3 {SECTION_WIDTH} {BUTTON_HEIGHT}]",
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
    
    with open(RTCONFIG_PATH, 'w') as f:
        f.write(content)
    
    print(f"✓ Updated rtconfig.txt")
    print(f"  Transport height: {TRANSPORT_HEIGHT}px")
    print(f"  Button size: {BUTTON_WIDTH}x{BUTTON_HEIGHT}px")
    print(f"  Button spacing: {BUTTON_SPACING}px")
    print(f"  Status width: {STATUS_WIDTH}px")


if __name__ == "__main__":
    update_rtconfig()
