# 🎵 Spotify TV Autoplay (Device Connect)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Spotify%20Web%20API-black?logo=spotify)
![Status](https://img.shields.io/badge/Status-Experimental-orange)

Automatically start a Spotify playlist on a chosen device using the
Spotify Web API.\
Includes device polling, optional volume fade-in, and environment-based
configuration.

> ⚠️ **Note:** Some Samsung TVs do not activate Spotify Connect unless
> the Spotify app was the last app used before powering off.

------------------------------------------------------------------------

## ✨ Features

-   🔍 Auto-detect Spotify Connect device\
-   ▶️ Start playback on target device\
-   🔀 Enable shuffle\
-   📈 Smooth volume fade-in\
-   ⚙️ Uses `.env` for configuration

------------------------------------------------------------------------

## 📦 Installation

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🔐 Creating Your Spotify App

1.  Go to https://developer.spotify.com/dashboard\
2.  Create app\
3.  Copy **Client ID** and **Client Secret**\
4.  Use redirect URI:

```{=html}
<!-- -->
```
    http://localhost:8888/callback

------------------------------------------------------------------------

## 🎧 Get Playlist ID

Share → Copy link → extract mid section:

    spotify:playlist:YOUR_ID

------------------------------------------------------------------------

## ⚙️ `.env`

    SPOTIPY_CLIENT_ID=xxx
    SPOTIPY_CLIENT_SECRET=xxx
    SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
    PLAYLIST_URI=spotify:playlist:xxx
    DEVICE_NAME=Your Device
    TARGET_VOLUME=30
    FADE_DURATION=20
    MAX_WAIT_SECONDS=180

------------------------------------------------------------------------

## 🚀 Run

``` bash
python main.py
```

------------------------------------------------------------------------

## 📸 Screenshots

Yes --- you can add screenshots!\
Just place them in your repo and reference like:

    ![Demo](screenshots/demo.png)

------------------------------------------------------------------------

## 📜 License

MIT License
