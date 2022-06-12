import requests
from bs4 import BeautifulSoup
import pixCookies

cookies = pixCookies.COOKIES

headers = pixCookies.HEADERS

response = requests.get('https://www.pixiv.net/ranking.php', cookies=cookies, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)