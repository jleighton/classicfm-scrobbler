import requests
from bs4 import BeautifulSoup
import pylast
import time
from alive_progress import alive_bar
import os

PreviousTrack = ""

#This should also work on Heart pages too I beleive
URL = "https://www.classicfm.com/radio/playlist/"

#UserAgent to use
UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"

#
headers = {
'User-Agent': UserAgent
}

x = 0
while x == 0:
    #Print the Previous track if we've already scrobbled something
    if PreviousTrack != "":
        print("Previous Track was %s" % PreviousTrack)

    #Get the page
    page = requests.get(URL, headers=headers)

    #HTML Elements Containing the Track and Artist Details
    TrackNameClass = "now-playing__text-content__details__track"
    ArtistNameClass = "now-playing__text-content__details__artist"

    #Load the page data
    soup = BeautifulSoup(page.content, "html.parser")

    #Find the first class with each name, get the text, then strip the whitespace (as the artist field contains weird line breaks)
    TrackName = soup.find('span', {'class' : TrackNameClass}).get_text().strip()
    ArtistName = soup.find('span', {'class' : ArtistNameClass}).get_text().strip()

    # Create API keys here https://www.last.fm/api/account/create
    API_KEY = "" 
    API_SECRET = ""

    # LastFM Credentials
    username = ""
    password_hash = pylast.md5("YourLastFmPassword")

    network = pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
        username=username,
        password_hash=password_hash,
    )

    #Check if we scrobbled this last time
    if PreviousTrack != TrackName:
        #Scrobble if previous track is not the same as the current track
        print("Scrobbling now: %s - %s" %(TrackName, ArtistName))
        network.scrobble(artist=ArtistName, title=TrackName, timestamp=int(time.time()))
    else:
        #Don't scrobble if we've just scrobbled in
        print("This track %s was already scrobbled" % TrackName)
    
    items=0

    #Lets now sleep for 100 seconds before running again
    #alive_bar prints the fancy progress bar
    with alive_bar(100) as bar: 
        while items < 100:
            time.sleep(1)
            bar.text('Until Next Scrobble')
            items = items + 1
            bar() 
    
    #Set Previous track to equal the current track so we can compare it in the next loop iteration
    PreviousTrack = TrackName
    #Clear the Screen
    os.system('clear')