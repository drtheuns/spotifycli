# Spotifycli Python3

This is a simple program to interact with Spotify over DBus.
It's based on [spotify-cli-linux](https://github.com/pwittchen/spotify-cli-linux/blob/master/spotifycli/spotifycli.py).

# Usage

## From CLI

```
$ ./spotifycli --help
spotify-cli is a command line interface for Spotify on Linux
usage:
  --help, -h		show help
  --status		shows status (curently playing song and artist)
  --play		start the music
  --pause		pauses the music
  --toggle		toggles the music
  --next		play the next song
  --prev		play the previous song

```

```
$ ./spotifycli --status
Hamferð - Fylgisflog
```

## From Python

```python
try:
    spotify = SpotifyBus()
except dbus.exceptions.DBusException:
    # Failed to connect to spotify dbus. Perhaps not running?
    sys.exit(2)

spotify.perform_action("Play")
spotify.perform_action("Next")
artist = spotify.artist[0]  # A track/album may have multiple artists, hence the list.
title = spotify.title
# or: artist, title = spotify.current_song()
```

The `SpotifyBus` class never protects the caller from exceptions, meaning those will have
to be handled by the caller. I don't expect any error other than `dbus.exceptions.DBusException`.

# Changes

The changes compared to the original spotify-cli are as follows:

- Upgrade to Python 3 as default
- Make it (arguably) a bit more reusable
- Remove volume control as that was not a part of Spotify (it was PulseAudio)
- Use `dbus-python` for the pause/play/etc actions rather than `subprocess`.

# Known issues

- Running this program with Python 2 might causes issues if you're playing a song
  with unicode (non-ascii) characters in it.
