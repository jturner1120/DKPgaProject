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
