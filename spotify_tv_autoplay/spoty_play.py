import time
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

PLAYLIST_URI = os.getenv("PLAYLIST_URI")
DEVICE_NAME = os.getenv("DEVICE_NAME", "Samsung").lower()
TARGET_VOLUME = int(os.getenv("TARGET_VOLUME", "30"))
FADE_DURATION = int(os.getenv("FADE_DURATION", "20"))
MAX_WAIT_SECONDS = int(os.getenv("MAX_WAIT_SECONDS", "180"))  # More time for TVs

# Spotify client
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="user-read-playback-state user-modify-playback-state"
    )
)


def list_visible_devices():
    """Return list of all device names visible to the Web API."""
    try:
        data = sp.devices()
        return [d.get("name", "") for d in data.get("devices", [])]
    except Exception:
        return []


def find_device_by_list():
    """Look for the TV in sp.devices()."""
    try:
        data = sp.devices()
        for d in data.get("devices", []):
            name = d.get("name", "").lower()
            if DEVICE_NAME in name:
                return d
    except Exception:
        pass
    return None


def find_device_by_playback():
    """Look for the TV in current_playback() if Spotify thinks playback is active."""
    try:
        pb = sp.current_playback()
        if not pb:
            return None
        device = pb.get("device")
        if not device:
            return None
        name = device.get("name", "").lower()
        if DEVICE_NAME in name:
            return device
    except Exception:
        pass
    return None


def wait_for_device():
    """Robust detection: try multiple endpoints until device appears."""
    print(f"Searching for TV '{DEVICE_NAME}'...")

    for second in range(MAX_WAIT_SECONDS):
        # Poll device list
        d1 = find_device_by_list()
        if d1:
            print(f"Found via device list: {d1['name']}")
            return d1

        # Poll playback info
        d2 = find_device_by_playback()
        if d2:
            print(f"Found via playback API: {d2['name']}")
            return d2

        # Debug output every second
        if second % 3 == 0:
            visible = list_visible_devices()
            print(f"Visible devices so far: {visible}")

        time.sleep(1)

    return None


def fade_in_volume(device_id: str, target_volume: int, duration: int):
    print(f"Fading from 0 to {target_volume}% over {duration} seconds…")

    target_volume = max(1, min(target_volume, 100))
    steps = target_volume
    delay = duration / steps if steps > 0 else 0.1

    for vol in range(1, target_volume + 1):
        try:
            sp.volume(vol, device_id=device_id)
        except Exception as e:
            print(f"Volume step {vol} failed: {e}")
        time.sleep(delay)

    print("Fade-in complete.")


def main():
    if not PLAYLIST_URI:
        print("Error: No playlist URI set.")
        return

    print("Waiting for TV to register with Spotify Connect…")
    device = wait_for_device()

    if not device:
        print("ERROR: TV did not appear in time.")
        return

    device_id = device["id"]
    device_name = device.get("name", "Unknown Device")
    print(f"Using device: {device_name} (ID: {device_id})")

    # Transfer playback
    print("Transferring playback…")
    sp.transfer_playback(device_id, force_play=True)
    time.sleep(2)

    # Shuffle
    print("Enabling shuffle…")
    try:
        sp.shuffle(True, device_id=device_id)
    except Exception:
        pass

    # Start playlist
    print("Starting playlist…")
    try:
        sp.start_playback(device_id=device_id, context_uri=PLAYLIST_URI)
    except Exception as e:
        print(f"Playback start failed: {e}")
        return

    time.sleep(2)

    # Fade volume
    fade_in_volume(device_id, TARGET_VOLUME, FADE_DURATION)

    print("🎶 Music is now playing on your TV with fade-in volume.")


if __name__ == "__main__":
    main()
