#!/usr/bin/env python3
"""
Copy FX files from LCS theme (keeping original teal color).
"""

import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
LCS_DIR = PROJECT_ROOT / "theme_source" / "LCS_Flat-707_unpacked"
BUILD_DIR = PROJECT_ROOT / "build" / "Default_7.0_DarkMinimal_unpacked"

# All FX-related files to copy from LCS
FX_FILES = [
    # TCP FX Text
    "track_fx_norm.png",
    "track_fx_dis.png", 
    "track_fx_empty.png",
    "track_fx_in_norm.png",
    "track_fx_in_empty.png",
    # TCP FX Text overlays
    "track_fx_norm_ol.png",
    "track_fx_dis_ol.png",
    "track_fx_empty_ol.png",
    # TCP Power horizontal
    "track_fxon_h.png",
    "track_fxoff_h.png",
    "track_fxempty_h.png",
    # TCP Power horizontal overlays
    "track_fxon_h_ol.png",
    "track_fxoff_h_ol.png",
    "track_fxempty_h_ol.png",
    # TCP Power vertical
    "track_fxon_v.png",
    "track_fxoff_v.png",
    "track_fxempty_v.png",
    # TCP Power vertical overlays
    "track_fxon_v_ol.png",
    "track_fxoff_v_ol.png",
    "track_fxempty_v_ol.png",
    # MCP FX Text
    "mcp_fx_norm.png",
    "mcp_fx_dis.png",
    "mcp_fx_empty.png",
    "mcp_fx_in_norm.png",
    "mcp_fx_in_empty.png",
    # MCP/Monitor power icons
    "monitor_fx_byp_on.png",
    "monitor_fx_byp_off.png",
    "monitor_fx_byp_byp.png",
    # Monitor FX text backgrounds
    "monitor_fx_on.png",
    "monitor_fx_off.png",
    "monitor_fx_byp.png",
]


def copy_fx_files():
    """Copy all FX files from LCS to build directory."""
    
    for name in FX_FILES:
        src = LCS_DIR / name
        if not src.exists():
            print(f"  ⚠ {name} not found in LCS")
            continue
            
        # Copy base file
        shutil.copy(src, BUILD_DIR / name)
        
        # Copy DPI variants
        for dpi in ["150", "200"]:
            src_dpi = LCS_DIR / dpi / name
            dst_dpi = BUILD_DIR / dpi / name
            if src_dpi.exists():
                dst_dpi.parent.mkdir(exist_ok=True)
                shutil.copy(src_dpi, dst_dpi)
        
        print(f"  ✓ {name}")


if __name__ == '__main__':
    print("=" * 50)
    print("FX Files - Copying from LCS (teal)")
    print("=" * 50)
    
    copy_fx_files()
    
    print("\n" + "=" * 50)
    print("Done!")
    print("=" * 50)
