import os
import sys
import shutil
import json
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
import argparse


# ----------------------------------------------------------------------
#  What folders to use with what extensions, it will create ifyou dont have them.
# ----------------------------------------------------------------------
DEFAULT_DESTINATIONS = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Music": [".mp3", ".wav", ".aac"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Installers": [".exe", ".msi", ".apk", ".deb"],
    "Scripts": [".py", ".js", ".sh", ".ps1"],
    "ISOs": [".iso", ".img"],
    "MailAttachments": [".eml", ".msg"],
}

CONFIG_FILE_NAME = "organizer_config.json"
#If there is no config file, this default will be used, no biggie.

# ----------------------------------------------------------------------
#  Detects download folder on different OSes
# ----------------------------------------------------------------------
def get_downloads_folder() -> Path:
    home = Path.home()
    win_default = home / "Downloads"
    mac_default = home / "Downloads"

    if sys.platform.startswith("win") and win_default.exists():
        return win_default

    if mac_default.exists():
        return mac_default

    return home


DOWNLOADS = get_downloads_folder()
LOG_DIR = DOWNLOADS / "ORGANIZER_LOGS"
LOG_FILE = LOG_DIR / "organizer.log"


# ----------------------------------------------------------------------
#  LOGGING
# ----------------------------------------------------------------------
def setup_logging(verbose: bool):
    LOG_DIR.mkdir(exist_ok=True)

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=2 * 1024 * 1024,  # 2MB
        backupCount=5,              # Keep last 5 logs
        encoding="utf-8",
    )

    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[handler],
    )


# ----------------------------------------------------------------------
#  LOAD CONFIG FILE
# ----------------------------------------------------------------------
def load_config(config_path: Path):
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    return {"destinations": DEFAULT_DESTINATIONS}


# ----------------------------------------------------------------------
#  SAFE UNIQUE MOVE DESTINATION
# ----------------------------------------------------------------------
def unique_destination(base_path: Path) -> Path:
    if not base_path.exists():
        return base_path

    stem = base_path.stem
    suffix = base_path.suffix
    counter = 1

    while True:
        new_name = base_path.parent / f"{stem} ({counter}){suffix}"
        if not new_name.exists():
            return new_name
        counter += 1


# ----------------------------------------------------------------------
#  SORTING LOGIC
# ----------------------------------------------------------------------
def sort_downloads(destinations: dict, dry_run: bool):
    logging.info("Starting organizer...")

    for item in DOWNLOADS.iterdir():
        if not item.is_file():
            continue

        ext = item.suffix.lower()
        moved = False

        for folder_name, extensions in destinations.items():
            if ext in extensions:
                dest_dir = DOWNLOADS / folder_name
                dest_dir.mkdir(exist_ok=True)

                target = unique_destination(dest_dir / item.name)

                if dry_run:
                    logging.info(f"[DRY RUN] Would move {item} → {target}")
                else:
                    try:
                        shutil.move(str(item), str(target))
                        logging.info(f"Moved: {item.name} → {target}")
                    except Exception as e:
                        logging.error(f"Error moving {item.name}: {e}")

                moved = True
                break

        if not moved:
            logging.info(f"Skipped (no rule): {item.name}")

    logging.info("Organizer finished.")


# ----------------------------------------------------------------------
#  CLEAN EMPTY DIRECTORIES
# ----------------------------------------------------------------------
def clean_empty_dirs():
    removed = 0
    for folder in DOWNLOADS.iterdir():
        if folder.is_dir() and folder.name not in ["ORGANIZER_LOGS"]:
            try:
                folder.rmdir()
                logging.info(f"Removed empty folder: {folder.name}")
                removed += 1
            except OSError:
                pass
    return removed


# ----------------------------------------------------------------------
#  CLI ARGUMENTS
# ----------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Downloads Organizer v2")
    p.add_argument("--dry-run", action="store_true", help="Preview actions without moving files")
    p.add_argument("--verbose", action="store_true", help="More detailed logs")
    p.add_argument("--clean-empty", action="store_true", help="Remove empty folders in Downloads")
    p.add_argument("--config", type=str, help="Path to a custom config JSON")
    return p.parse_args()


# ----------------------------------------------------------------------
#  MAIN ENTRY
# ----------------------------------------------------------------------
if __name__ == "__main__":
    args = parse_args()

    config_path = Path(args.config) if args.config else DOWNLOADS / CONFIG_FILE_NAME
    config = load_config(config_path)

    setup_logging(args.verbose)

    sort_downloads(
        destinations=config.get("destinations", DEFAULT_DESTINATIONS),
        dry_run=args.dry_run,
    )

    if args.clean_empty:
        clean_empty_dirs()
        logging.info("Cleanup finished.")
