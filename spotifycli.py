#!/usr/bin/env python3
import getopt
import sys

import dbus

DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"
MEDIA_INTERFACE = "org.mpris.MediaPlayer2"
MEDIA_OBJECT_PATH = "/org/mpris/MediaPlayer2"
MEDIA_PLAYER_INTERFACE = MEDIA_INTERFACE + ".Player"
SPOTIFY_INTERFACE = MEDIA_INTERFACE + ".spotify"


class SpotifyBus:

    def __init__(self):
        self.session_bus = dbus.SessionBus()
        self.spotify_bus = self.session_bus.get_object(
            SPOTIFY_INTERFACE,
            MEDIA_OBJECT_PATH
        )
        self.spotify_properties = dbus.Interface(
            self.spotify_bus,
            DBUS_PROPERTIES
        )
        self.metadata = self.spotify_properties.Get(
            MEDIA_PLAYER_INTERFACE,
            "Metadata"
        )
        self.spotify_player = dbus.Interface(
            self.spotify_bus,
            MEDIA_PLAYER_INTERFACE
        )

    def current_song(self):
        return self.artist[0], self.title

    def perform_action(self, action):
        getattr(self.spotify_player, action)()

    def __getattr__(self, name):
        """Allow for easy fetching of attributes from the metadata"""
        # All items in metadata are prefixed with xesam, but we don't
        # want the caller to have to bother with that jazz
        key = 'xesam:' + name
        return self.metadata[key] if key in self.metadata else None

    def __contains__(self, key):
        return 'xesam:' + key in self.metadata


def show_help():
    print("""spotify-cli is a command line interface for Spotify on Linux
usage:
  --help, -h\t\tshow help
  --status\t\tshows status (curently playing song and artist)
  --play\t\tstart the music
  --pause\t\tpauses the music
  --toggle\t\ttoggles the music
  --next\t\tplay the next song
  --prev\t\tplay the previous song
    """)


def print_status(artist, album):
    print("{} - {}".format(artist, album))


def main():
    # These could also be defined as actual functions, but they're
    # too small to be worth the hassle in my opinion.
    actions = {
        "help": lambda _: show_help(),
        "status": lambda bus: print_status(*bus.current_song()),
        "play": lambda bus: bus.perform_action("Play"),
        "pause": lambda bus: bus.perform_action("Pause"),
        "toggle": lambda bus: bus.perform_action("PlayPause"),
        "next": lambda bus: bus.perform_action("Next"),
        "previous": lambda bus: bus.perform_action("Previous"),
    }

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:", actions.keys())
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    try:
        spotify = SpotifyBus()
    except dbus.exceptions.DBusException:
        print("spotify is off")
        return

    for opt, arg in opts:
        opt = opt.replace('-', '')
        if opt not in actions:
            show_help()
        else:
            actions[opt](spotify)


if __name__ == '__main__':
    main()
