import urllib.request as urlreq
import urllib.error as urlerror
import re
import json
from pprint import pprint
from bs4 import BeautifulSoup as BS

debugging = True

def main():
    seedpage = getseedpage()
    myPlayerLinks = pulloutplayerlinks(seedpage)
    linkparts = splitlinks(myPlayerLinks)
    jsonstatlinks = generatejsonstatlinks(linkparts)
    jsonfinishlinks = generatejsonfinishlinks(linkparts)
    decodedstats = readjsontopy(jsonstatlinks)
    decodedfinish = readjsontopy(jsonfinishlinks)


def getseedpage():
    seedPage = "http://www.pgatour.com/players.html"
    pgaPlayersPage = getPageData(seedPage)
    souptogo = BS(pgaPlayersPage, 'html.parser')
    return souptogo

def pulloutplayerlinks(playersoup):
    playerlinks  = playersoup.find_all('a', href=re.compile('^/content/pgatour/players/player'))
    del playerlinks[:5]
    return playerlinks


def splitlinks(links):
    storage = []
    for link in links:
        slink = str(link)
        storage.append(slink.split('.'))
    return storage


def generatejsonstatlinks(linkparts):
    storage = []
    for linkpart in linkparts:
        tempstatsjson = "http://www.pgatour.com/data/players/" + linkpart[1] + "/2017stat.json"
        storage.append(tempstatsjson)
    return storage


def generatejsonfinishlinks(linkparts):
    storage = []
    for linkpart in linkparts:
        tempfinshjson = "http://www.pgatour.com/data/players/" + linkpart[1] + "/2017results.json"
        storage.append(tempfinshjson)
    return storage


def getPageData(url):
    with urlreq.urlopen(url) as url:
        return url.read()


def readjsontopy(jsonlinks):
    storage = []
    if debugging == True:
        for link in jsonlinks[1:5]:
            try:
                with urlreq.urlopen(link) as url:
                    data = json.loads(url.read().decode())
                    storage.append(data)
            except urlerror.HTTPError as err:
                if err.code == 404:
                    continue
                else:
                    raise
    else:
        for link in jsonlinks:
            try:
                with urlreq.urlopen(link) as url:
                    data = json.loads(url.read().decode())
                    storage.append(data)
            except urlerror.HTTPError as err:
                if err.code == 404:
                    continue
                else:
                    raise
    return storage

#for use in dubugging to find json pages
def printrawhtmlplayerpage():
    playerpage = "http://www.pgatour.com/players/player.29745.tyler-aldridge.html"
    toviewplayerhtml = getPageData(playerpage)
    playertesthtmlsoup = BS(toviewplayerhtml, 'html.parser')
    print(playertesthtmlsoup.prettify())



if __name__ == "__main__":
    main()

"""
Scoring system for DK PGA:

    Double Eagle (DBe): +20 PTs
    Eagle (EAG): +8 PTs
    Birdie (BIR): +3 PTs
    Par (PAR): +0.5 PTs
    Bogey (BOG): -0.5 PTs
    Double Bogey (DBB): -1 PT
    Worse than Double Bogey (DBW): -1 PT

    1st: 30 PTs
    2nd: 20 PTs
    3rd: 18 PTs
    4th: 16 PTs
    5th: 14 PTs
    6th: 12 PTs
    7th: 10 PTs
    8th: 9 PTs
    9th: 8 PTs
    10th: 7 PTs
    11th–15th: 6 PTs
    16th–20th: 5 PTs
    21st–25th: 4 PTs
    26th–30th: 3 PTs
    31st–40th: 2 PTs
    41st-50th: 1 PTs

    Streak of 3 Birdies of Better (MAX 1 Per Round) (BIR3+): +3 PTs
    Bogey Free Round (BOFR): +3 PTs
    All 4 Rounds Under 70 Strokes (A4U70): +5 PTs
    Hole in One (ACE): +10 PTs

    stats I like to start:
    Driving acc
    Driving Dist
    gir
    putts per green



"""
# player stats in json http://www.pgatour.com/data/players/{pid}/{year}stat.json