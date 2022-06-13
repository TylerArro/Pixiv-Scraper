import requests
from bs4 import BeautifulSoup
import pixCookies

cookies = pixCookies.COOKIES
headers = pixCookies.HEADERS
imgHeaders = pixCookies.IMG_HEADERS
imageLimit = 1
urlBase = "https://www.pixiv.net"
response = requests.get('https://www.pixiv.net/ranking.php', cookies=cookies, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
#print(soup.prettify())

imageHTML = soup.find_all("a",class_="work _work",limit=imageLimit)

for x in imageHTML:
    #looks like im going to have to use selenium here to get the image url

    #print(x.attrs['href'])

    urlSuffix = x.attrs['href']
    print(urlBase + urlSuffix)

    responseImg = requests.get(urlBase + urlSuffix, cookies=cookies, headers=imgHeaders)
    soupImg = BeautifulSoup(responseImg.content, 'html.parser')
    print(soupImg.prettify())

    #imageURL = soupImg.find_all("div" , id="root")
    #print(imageURL)

