from urllib.request import urlopen as uRequest
from urllib.request import Request
from bs4 import BeautifulSoup as soup
from collections import OrderedDict 
from datetime import datetime  
from datetime import timedelta
import time

dateFormat = '%Y-%m-%d'

startDatestring = '2021-12-04'
endDatestring = '2021-12-18'
maxPosition = 100

currentDate = datetime.strptime(startDatestring, dateFormat)
endDate = datetime.strptime(endDatestring, dateFormat)

dateList = []
while (currentDate <= endDate):
    dateList.append(currentDate.strftime(dateFormat))
    currentDate = currentDate + timedelta(days=7)

songList = {}
positionList = {}

filename = 'billboard_hot_100_2022_history.csv'
f = open(filename, 'w') # w = write

headers = 'Song,Artist,' + ','.join(map(str, dateList)) + '\n'
f.write(headers)

for date in dateList:
    print('Retrieving data for ' + date)

    url = 'https://www.billboard.com/charts/hot-100/' + date

    # Opening up connection, grabbing the page
    uClient = uRequest(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
    page_html = uClient.read() # Offloads content into a variable
    uClient.close() # Close the client

    # HTML parsing
    page_soup = soup(page_html, "html.parser")

    # Grabs all information related to the top 100 songs
    containers = page_soup.findAll('div', {'class': 'o-chart-results-list-row-container'})

    chart_position = 1

    # Loops through each container
    for container in containers:
        # entry shell
        entry = container.find('li', {'class': 'lrv-u-width-100p'}).find('li', {'class': 'o-chart-results-list__item'})

        # Grabs the song name
        song = entry.find('h3', {'id': 'title-of-a-story'}).text.strip()

        # Grabs the artist name
        artist = entry.find('span').text.strip()

        songArtistKey = artist.lower() + '-' + song.lower()
        if songArtistKey not in songList.keys():
            songList[songArtistKey] = {'song': song, 'artist': artist}

        positionKey = song.lower() + '-' + artist.lower() + '-' + date.lower()
        positionList[positionKey] = chart_position

        chart_position += 1
        if chart_position > maxPosition:
            break

    time.sleep(10)

sorted_songList = OrderedDict(sorted(songList.items()))

for song in sorted_songList.values():
    songPositionList = []
    for date in dateList:
        positionKey = song.get('song').lower() + '-' + song.get('artist').lower() + '-' + date.lower()
        datePosition = positionList.get(positionKey, '-')
        songPositionList.append(datePosition)
    f.write('\"' + song.get('song') + '\",\"' + song.get('artist') + '\",\"' + '\",\"'.join(map(str, songPositionList)) + '\"\n')

f.close()