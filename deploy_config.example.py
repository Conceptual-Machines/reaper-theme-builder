"""
Deployment configuration for REAPER theme builder.

Copy this file to 'deploy_config.py' and customize the paths for your system.
The deploy_config.py file is gitignored so you can have your own local settings.

If deploy_config.py doesn't exist, the build will only create the .ReaperThemeZip
file in the project root without deploying it anywhere.
"""

from pathlib import Path

# List of REAPER ColorThemes directories to deploy to
# Add or remove paths as needed for your setup
DEPLOY_DIRS = [
    # Example: Portable REAPER installation
    # Path("/Users/YourUsername/path/to/reaper-portable/ColorThemes"),

    # Example: System REAPER installation (macOS)
    # Path.home() / "Library/Application Support/REAPER/ColorThemes",

    # Example: System REAPER installation (Windows)
    # Path.home() / "AppData/Roaming/REAPER/ColorThemes",

    # Example: System REAPER installation (Linux)
    # Path.home() / ".config/REAPER/ColorThemes",
]
