import spotipy
import yt_dlp as youtube_dl
import os
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch

CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_tracks_from_playlist(playlist_url):
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    
    offset = 0
    song_details = []
    
    while True:
        results = sp.playlist_items(playlist_id, offset=offset, limit=100)
        tracks = results['items']
        
        if not tracks:
            break

        for track in tracks:
            song_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            song_details.append(f"{song_name} von {artist_name}")

        offset += 100

    return song_details

def get_youtube_url(song_name, artist_name):
    query = f"{song_name}, {artist_name}"
    results = YoutubeSearch(query, max_results=1).to_dict()
    if results:
        return f"https://www.youtube.com{results[0]['url_suffix']}"
    return None

def download_as_mp3(youtube_url, output_path='downloads'):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        video_title = info_dict['title']

    target_file_webm = os.path.join(output_path, f"{video_title}.webm")
    target_file_m4a = os.path.join(output_path, f"{video_title}.m4a")

    if os.path.exists(target_file_webm) or os.path.exists(target_file_m4a):
        print(f"Datei für {video_title} bereits heruntergeladen. Überspringen...")
        return

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
