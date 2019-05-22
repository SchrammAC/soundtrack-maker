from bs4 import BeautifulSoup

import requests, json, re

artistname = 'Cage The Elephant'

songurl = []
lyricdata = []

artistlink = 'https://web.archive.org/web/20161104213857/http://www.azlyrics.com/c/cagetheelephant.html'


linkend = 'cagetheelephant' #example: rollingstones


header = { 'User-Agent':'data project'}

page = requests.get(artistlink, headers=header)
page_html = page.text
soup = BeautifulSoup(page_html, "html.parser")
songlist= soup.find_all("a", attrs={"href": re.compile("lyrics/"+linkend)})

for song in songlist:
    songurl.append("https://web.archive.org"+song['href'])
#    songurl.append("https://www.azlyrics.com"+song['href'])

for url in songurl:
    lyricpage = requests.get(url, headers=header)
    lyricpage_html = lyricpage.text
    lyricsoup = BeautifulSoup(lyricpage_html, "html.parser")
    lyricbody = lyricsoup.find("br")
    lyricdict = {artistname :lyricbody.text}
    lyricdata.append(lyricdict)

with open('Rock/cagetheelephant.json', 'w') as file:
    file.write(json.dumps(lyricdata,indent=4))


