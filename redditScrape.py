import os

import lxml.etree as ET
import requests
from bs4 import BeautifulSoup

rssRedditURL = "https://www.reddit.com/r/MicrosoftRewards/search.rss?sort=new&restrict_sr=on&q=flair%3AMail%2BPoints"

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}

xmlData = requests.get(rssRedditURL, headers=headers).text

with open("tempFileDelete.txt", "wb") as xmlThing:
    xmlThing.write(xmlData.encode())

tree = ET.parse("tempFileDelete.txt")
root = tree.getroot()

os.remove("tempFileDelete.txt")
linkList = []

tag = "{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}content"
for content in root.findall(tag):
    soup = BeautifulSoup(content.text, "lxml")
    for link in soup.findAll("a"):
        url = link.get("href")
        if url and "http" in url and ("/aka.ms" in url
                                      or "/e.microsoft" in url):
            linkList.append(url)

with open("email_links.txt", "w") as filehandle:
    for listitem in linkList:
        filehandle.write("%s\n" % listitem)

print("Saved %s links from reddit" % len(linkList))
