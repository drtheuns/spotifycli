# Spotifycli Python3

This is a simple program to interact with Spotify over DBus.
It's based on [spotify-cli-linux](https://github.com/pwittchen/spotify-cli-linux/blob/master/spotifycli/spotifycli.py).

# Changes

The changes compared to the original spotify-cli are as follows:

- Upgrade to Python 3 as default
- Make it (arguably) a bit more reusable
- Remove volume control as that was not a part of Spotify (it was PulseAudio)
- Use `dbus-python` for the pause/play/etc actions rather than `subprocess`.

# Known issues

- Running this program with Python 2 might causes issues if you're playing a song
  with unicode (non-ascii) characters in it.
