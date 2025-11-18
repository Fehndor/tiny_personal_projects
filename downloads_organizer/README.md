# Downloads Organizer v2.1

A lightweight script that automatically sorts files in your **Downloads** folder into clean category subfolders (Documents, Images, Installers, etc.).  
Includes log rotation, dry-run mode, unique filename handling, and optional cleanup of empty folders.  
Compatible with Windows, macOS, and Linux.

---

## Features
- Automatically sorts files in the Downloads directory by extension  
- Creates category folders only when needed  
- Optional cleanup of empty folders  
- Unique file naming to avoid overwrites  
- Rotating log files stored in `ORGANIZER_LOGS/`  
- Configurable categories via `organizer_config.json`  
- Dry-run and verbose modes for safe testing  
- Does not recurse into subfolders (safe by design)

---

## Default Categories
Editable through the config file.

| Category   | Extensions                                 |
|------------|---------------------------------------------|
| Documents  | .pdf, .doc, .docx, .txt, .xlsx, .csv       |
| Images     | .jpg, .jpeg, .png, .gif, .webp             |
| Archives   | .zip, .rar, .7z, .tar, .gz                 |
| Music      | .mp3, .wav, .aac                           |
| Videos     | .mp4, .mkv, .mov, .avi                     |
| Installers | .exe, .msi, .apk, .deb                     |
| Scripts    | .py, .js, .sh, .ps1                        |
| ISOs       | .iso, .img                                 |

---

## Installation

1. Save the script (`downloads_organizer_v2_1.py`) anywhere on your machine.
2. Ensure Python 3 is installed.

Check Python version:

### Windows:
```
py --version
```

### macOS / Linux:
```
python3 --version
```

---

## Configuration File (`organizer_config.json`)

Place in:

```
~/Downloads/organizer_config.json
```

Example:

```json
{
  "_comment": "Extension categories for the organizer.",
  "destinations": {
    "Documents": [".pdf", ".docx", ".txt"],
    "Images": [".jpg", ".png"],
    "Videos": [".mp4", ".mov"]
  }
}
```

If no config file is found, default categories are used.

---

## Usage

### Basic run:
```
python downloads_organizer_v2_1.py
```

### Preview without moving files:
```
python downloads_organizer_v2_1.py --dry-run
```

### Verbose logging:
```
python downloads_organizer_v2_1.py --verbose
```

### Remove empty folders:
```
python downloads_organizer_v2_1.py --clean-empty
```

### Use a custom config file:
```
python downloads_organizer_v2_1.py --config C:\path\config.json
```

---

## Logging

Logs are written to:

```
~/Downloads/ORGANIZER_LOGS/organizer.log
```

- Log rotates after reaching 2 MB  
- Keeps 5 backup logs  
- Logs everything sorted, skipped, or errors encountered

---

## Automation

### Windows (Task Scheduler)

1. Open Task Scheduler  
2. Create Basic Task  
3. Trigger: Daily  
4. Action → Start a Program  
5. Program:
```
python
```
6. Arguments:
```
C:\path\to\downloads_organizer_v2_1.py
```

### macOS / Linux (cron)
```
crontab -e
```

Add:
```
0 9 * * * /usr/bin/python3 /path/to/downloads_organizer_v2_1.py
```

---

## License
Free to use and modify.

