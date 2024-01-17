import datetime

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ---------------------------- User Data ------------------------------- #
URL = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = "a4dd0a1da08247039400af348f714381"
CLIENT_SECRET = "65b2ff5b98244bfe9158f0f002c2c78c"
SPOTIPY_REDIRECT_URI = "http://example.com"
SCOPE = "playlist-modify-private"
USERNAME = "TEETHGRINDER_GB"
# ----------------------- Choosing a date and validating input ------------------------- #
date_is_chosen = False
global chosen_date
while not date_is_chosen:
    try:
        print("Year (YYYY):")
        year = input()
        print("Month (MM):")
        month = input()
        print("Day (DD):")
        day = input()
        chosen_date = datetime.date(year=int(year), month=int(month), day=int(day))
        if chosen_date > datetime.date.today():
            print("Can't see into the future, try again")
        elif chosen_date < datetime.date(year=1958, month=8, day=4):
            print("The earliest top 100 is 1958-08-04, try again")
        else:
            date_is_chosen = True
    except:
        print("Invalid input, try again")

date = str(chosen_date)
print("You have chosen this date: " + date)

# ---------------------------- Scraping ------------------------- #
response = requests.get(URL + date + "/")
web_page = response.text
soup = BeautifulSoup(web_page, 'html.parser')

#scraping names of the songs
song_names = soup.select("li ul li h3")
songs = [song.getText().strip() for song in song_names]

#scraping band names
band_names = soup.select("li ul li span")
band_names = band_names[::7]
bands = [band.getText().strip() for band in band_names]

tracks = list(zip(songs, bands))
print("------------------\n")
print("Top 100 " + date + ":")
for track in tracks:
    print(track)
# ---------------- Creating Spotify playlist ------------------- #
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-public",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=USERNAME,
    )
)

user_id = sp.current_user()["id"]
print("------------------\n")
print("Creating playlist")
name_of_playlist = f"Billboard top 100 {date}"
playlist_id = sp.user_playlist_create(user_id, name_of_playlist, public=True, description='playing with Spotipy')["id"]
song_urls = []
for n in range(99):
    result = sp.search(q=f"track:{tracks[n][0]}, artist:{tracks[n][1]}", limit=1, offset=0, type='track', market=None)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_urls.append(uri)
    except IndexError:
        print(f"{tracks[n][0]} by {tracks[n][1]} isn't found")

sp.playlist_add_items(playlist_id,song_urls)
print("------------------\n")
print(f"I have found {len(song_urls)} songs")
