<h1>Billboard Top 100 to Spotify playlist</h1>
This app allows you to create a Spotify playlist from Billboard's Top 100 for any chosen date from 1958-08-04 till today.

<h3>Steps:</h3>
<ol>
  <li>app asks user to choose a date from 1958-08-04 till today and validates user's input using datetime.
</li>
  <li>scrapes the top 100 songs from https://www.billboard.com/charts/hot-100/ (titles and artist names) for chosen date using the BeautifulSoup library and prints this list of pairs song - artist.</li>
  <li>creates a Spotify playlist using the Spotipy library, adds tracks from the list and also prints a list of songs which are not found</li>
</ol>

<h3>Demo</h3>

![](https://github.com/GeorgiyBereza/BillboardTop100Spotify/blob/main/spotidemo.gif)
