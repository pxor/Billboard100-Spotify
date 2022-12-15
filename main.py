import os
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

DATE = input("Which year do you want to travel to? Type the date in this format 'YYYY-MM-DD': ")
YEAR = DATE.split("-")[0]

USER_ID = os.environ.get("USER_ID")

# Scrape Billboard Top 100
response = requests.get(f"https://www.billboard.com/charts/hot-100/{DATE}")
website_data = response.text

soup = BeautifulSoup(website_data, "html.parser")
song_chart = soup.find("div", class_="chart-results // lrv-a-wrapper lrv-u-padding-lr-00@mobile-max")
songs = song_chart.find_all("h3")
songs_list = []

# Create song list
for song in songs[2::4]:
    song_name = song.getText().strip()
    songs_list.append(song_name)

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

song_uri_list = []

# Search Spotify for the song URI
for song in songs_list:
    try:
        song_uri = sp.search(q='track: ' + song + ' year: ' + YEAR, type="track", limit=1)
        song_uri_list.append(song_uri["tracks"]["items"][-1]["uri"])
    except IndexError:
        print(f"{song} not available!")

# Set the scope of the use
scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Create private playlist in Spotify
playlist_id = sp.user_playlist_create(
    user=USER_ID,
    name=f"{DATE} Billboard 100",
    public=False,
    collaborative=False,
    description="",
    )

# Add tracks to the playlist using its id
sp.playlist_add_items(
    playlist_id=playlist_id["id"],
    items=song_uri_list,
    position=None,
    )
