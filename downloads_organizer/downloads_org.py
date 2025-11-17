import os
import shutil
from pathlib import Path
import sys
import winreg




# Function to get the Downloads folder path on Windows
def _get_windows_downloads_from_registry():
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
        ) as key:
            value, _ = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")
            return Path(os.path.expandvars(value))
    except Exception:
        return None

def get_downloads_folder():
    if sys.platform.startswith("win"):
        p = _get_windows_downloads_from_registry()
        if p and p.exists():
            return p
    p = Path.home() / "Downloads"
    if p.exists():
        return p
    return Path.home()

# You can define the Downloads folder path here, if you dont want to use the default
DOWNLOADS = get_downloads_folder()




# Define destination folders
# Creates them if you dont already have them
DESTINATIONS = {
    "Docs": [".pdf", ".doc", ".docx", ".txt"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Archives": [".zip", ".rar", ".7z"],
    "Music": [".mp3", ".wav"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Installers": [".exe", ".msi"],
    "Scripts": [".py", ".js", ".sh"],
    "ISOs": [".iso", ".img"],
}

def sort_downloads():
    for item in DOWNLOADS.iterdir():
        if item.is_file():
            extension = item.suffix.lower()

            moved = False

            # Check each extension group
            for folder, extensions in DESTINATIONS.items():
                if extension in extensions:
                    target_dir = DOWNLOADS / folder
                    target_dir.mkdir(exist_ok=True)

                    # Move file
                    shutil.move(str(item), str(target_dir / item.name))
                    print(f"Moved: {item.name} → {folder}/")
                    moved = True
                    break

            if not moved:
                print(f"Skipped: {item.name}")

if __name__ == "__main__":
    sort_downloads()
    print("\nSorting complete.")
