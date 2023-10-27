import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")


class Spotify:
    def __init__(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope="playlist-modify-private",
                redirect_uri="http://example.com",
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
                show_dialog=True,
                cache_path="token.txt",
                username="dozkanpyt"
            )
        )

    def create_list(self, song_names, date):
        user_id = self.sp.current_user()["id"]

        # Searching Spotify for songs by title
        song_uris = []
        year = date.year
        for song in song_names:
            result = self.sp.search(q=f"track:{song} year:{year}", type="track")
            print(result)
            try:
                uri = result["tracks"]["items"][0]["uri"]
                song_uris.append(uri)
            except IndexError:
                print(f"{song} doesn't exist in Spotify. Skipped.")

        # Create Playlist
        playlist = self.sp.user_playlist_create(user=user_id, name=f"{date} BILBOARD 100", public=False)
        #print(playlist['external_urls']['spotify'])
        # Adding track into playlist
        self.sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
        return playlist['external_urls']['spotify']
