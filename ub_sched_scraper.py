from bs4 import BeautifulSoup
import requests
from os.path import exists

# Request website and download HTML
url = 'https://www.buffalo.edu/class-schedule?semester=spring'
request = requests.get(url)
content = request.text 

if (not exists("content.txt")):
    contentFile = open('content.txt', 'w')
    contentFile.write(content)
    contentFile.close() 
    #print(content)

soup = BeautifulSoup(content, "html.parser")

if (not exists("contentsoup.txt")):
    contentSoupFile = open('contentsoup.txt', 'w')
    contentSoupFile.write(str(soup))
    contentSoupFile.close()
    #print(BeautifulSoup)



