import spotipy
import spotipy.util as util
import lyricsgenius
import json
import re


def get_title(scope, username, client_id, client_secret, redirect_uri):
    token = util.prompt_for_user_token(
        username=username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )

    spotify = spotipy.Spotify(auth=token)
    current_track = spotify.current_user_playing_track()

    artist = current_track["item"]["artists"][0]["name"]
    name = current_track["item"]["name"]

    return f"{name} - {artist}"


def get_name(scope, username, client_id, client_secret, redirect_uri):
    token = util.prompt_for_user_token(
        username=username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )

    spotify = spotipy.Spotify(auth=token)
    current_track = spotify.current_user_playing_track()

    name = current_track["item"]["name"]

    return f"{name}"


def get_lyrics(
    scope, username, client_id, client_secret, redirect_uri, client_access_token
):
    genius = lyricsgenius.Genius(client_access_token=client_access_token)
    token = util.prompt_for_user_token(
        username=username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )

    spotify = spotipy.Spotify(auth=token)
    current_track = spotify.current_user_playing_track()

    artist = current_track["item"]["artists"][0]["name"]
    name = current_track["item"]["name"]

    if "Remaster" in name:
        name = re.sub(r"Remaster\b", "", name)
        name = name[: name.index("-")].strip()

    song = genius.search_song(title=name, artist=artist)

    try:
        lyrics = {"lyrics": song.lyrics}
        json_object = json.dumps(lyrics, indent=4)

        with open("lyrix/lyrics.json", "w") as outfile:
            outfile.write(json_object)
    except AttributeError:
        print("This song's lyrics cannot be found!")

        json_object = json.dumps(
            {"lyrics": "No lyrics could be found on Genius for this song."}, indent=4
        )

        with open("lyrix/lyrics.json", "w") as outfile:
            outfile.write(json_object)
