import spotipy
import yt_dlp as youtube_dl
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch

CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_tracks_from_playlist(playlist_url):
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    results = sp.playlist(playlist_id)
    tracks = results['tracks']['items']
    song_details = []
    for track in tracks:
        song_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        song_details.append(f"{song_name} von {artist_name}")
    return song_details

def get_youtube_url(song_name, artist_name):
    query = f"{song_name}, {artist_name}"
    results = YoutubeSearch(query, max_results=1).to_dict()
    if results:
        return f"https://www.youtube.com{results[0]['url_suffix']}"
    return None

def download_as_mp3(youtube_url, output_path='downloads'):
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([youtube_url])


def main():
    link = input("Bitte geben Sie den Link ein (Spotify/SoundCloud): ")

    if "spotify.com" in link:
        songs = get_tracks_from_playlist(link)
        for song in songs:
            song_name, artist_name = song.split(" von ")
            youtube_url = get_youtube_url(song_name, artist_name)
            if youtube_url:
                print(f"{song} -> {youtube_url}")
                download_as_mp3(youtube_url)
            else:
                print(f"{song} -> Keine YouTube-URL gefunden.")
    elif "soundcloud.com" in link:
        download_as_mp3(link)
    else:
        print("Ungültiger Link oder nicht unterstützte Quelle.")

if __name__ == "__main__":
    main()
