import spotipy
from commands import *

password = Str.input_pass()

client_id = [29, -23, -3, -21, -56, -9, -45, 1, 16, 67, -14, -16, -53, 26, -9, -59, -41, 51, 67, 18, 31, -21, -4,
             -20, -62, -10, -44, 0, 16, 66, -18, 29]
client_id = Str.decrypt(client_id, password)

client_secret = [32, -19, -48, -15, -61, -51, 0, 3, 18, 21, -20, 28, -53, 30, -60, -55, 0, 49, 19, 16, -20, -14,
                 -7, 31, -11, -7, -42, 3, 16, 22, -21, -19]
client_secret = Str.decrypt(client_secret, password)

del password

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id=client_id,
                                                              client_secret=client_secret,
                                                              redirect_uri="https://spotipy.egigoka.me",
                                                              scope="ugc-image-upload "
                                                                    "user-read-recently-played "
                                                                    "user-read-playback-position "
                                                                    "user-top-read "
                                                                    "playlist-modify-private "
                                                                    "playlist-read-collaborative "
                                                                    "playlist-read-private "
                                                                    "playlist-modify-public "
                                                                    "streaming "
                                                                    "app-remote-control "
                                                                    "user-read-email "
                                                                    "user-read-private "
                                                                    "user-follow-read "
                                                                    "user-follow-modify "
                                                                    "user-library-modify "
                                                                    "user-library-read "
                                                                    "user-read-currently-playing "
                                                                    "user-read-playback-state "
                                                                    "user-modify-playback-state"))

del client_id
del client_secret

# select playlist
playlists = sp.current_user_playlists()
selected_playlist = None
for idx, playlist in enumerate(playlists['items']):
    print(idx, playlist['name'])
    if playlist['name'].lower() == "liked songs (public, managed)":
        selected_playlist = playlist['uri']
        Print.colored(f"selected {playlist['name']}", "green")
        break

if not selected_playlist:
    selected_playlist = CLI.get_int("select album to add liked songs")
    selected_playlist = playlists['items'][selected_playlist]['uri']

cnt = 0

while True:
    # get 50 songs from selected playlist
    results = sp.playlist_items(playlist_id=selected_playlist, offset=0)

    cnt += len(results['items'])
    Print.rewrite("removed", cnt, "songs")
    if not results['items']:
        break

    uris = []
    for idx, item in enumerate(results['items']):
        track = item['track']
        cnt += 1
        # print(idx + offset + 1, track['artists'][0]['name'], " – ", track['name'], track['uri'])
        # Print.prettify(track)
        uris.append(track['uri'])

    # remove all songs from playlist
    sp.playlist_remove_all_occurrences_of_items(selected_playlist, uris)

offset = 0
cnt = 0

File.delete("Liked songs.log")
File.delete("Liked songs uris.log")
while True:
    # get 50 songs from liked playlist
    results = sp.current_user_saved_tracks(limit=50, offset=offset)
    if not results['items']:
        break
    uris = []
    for idx, item in enumerate(results['items']):
        track = item['track']
        cnt = idx + offset + 1
        # print(idx + offset + 1, track['artists'][0]['name'], " – ", track['name'], track['uri'])
        File.write("Liked songs.log", track['artists'][0]['name'] + " – " + track['name'] + " " + track['uri'] + newline, mode="a")
        File.write("Liked songs uris.log", track['uri'] + newline, mode = "a")
        # Print.prettify(track)
        uris.append(track['uri'])

    # remove songs if they in playlist
    sp.playlist_remove_all_occurrences_of_items(selected_playlist, uris)

    # add songs to playlist
    sp.playlist_add_items(selected_playlist, uris, position=offset)
    Print.rewrite(f"processed {cnt} songs")
    offset += len(results['items'])

print(f"processed {cnt} songs")
