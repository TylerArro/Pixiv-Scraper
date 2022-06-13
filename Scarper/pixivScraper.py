
import requests
from bs4 import BeautifulSoup
import pixCookies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


wdOptions = webdriver.ChromeOptions()
wdOptions.add_argument('--ignore-certificate-errors')
#wdOptions.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=wdOptions)

cookies = pixCookies.COOKIES
headers = pixCookies.HEADERS
imageLimit = 1
urlBase = "https://www.pixiv.net"

#-------------------FUNCTIONS-------------------------------------------------------------------

def getImageURLS():
    response = requests.get('https://www.pixiv.net/ranking.php', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup.prettify())

    imageHTML = soup.find_all("a",class_="work _work",limit=imageLimit)

    return imageHTML

def getImages(ImagesURLS):
    for x in ImagesURLS:
        #looks like im going to have to use selenium here to get the image url

        #print(x.attrs['href'])

        urlSuffix = x.attrs['href']
        print(urlBase + urlSuffix)

        driver.get(urlBase + urlSuffix)
        elem = driver.find_element_by_class_name("sc-1qpw8k9-3 eFhoug gtm-expand-full-size-illust")
        print(elem.get_attribute("href"))
        driver.close()

        # responseImg = requests.get(urlBase + urlSuffix, cookies=cookies, headers=imgHeaders)
        # soupImg = BeautifulSoup(responseImg.content, 'html.parser')
        # print(soupImg.prettify())

        #imageURL = soupImg.find_all("div" , id="root")
        #print(imageURL)

def initDriver():
    driver.get(urlBase)
    driver.find_element(By.CLASS_NAME,'signup-form__submit--login').click()

    try:
        username  = WebDriverWait(driver,timeout=3).until(lambda d: d.find_element(By.CLASS_NAME,"degQSE"))
        username.clear()
        username.send_keys(pixCookies.PIXEMAIL)
    except Exception as e:
        driver.close()
        print(e)

    try:
        password = driver.find_element_by_class_name("hfoSmp")
        password.clear()
        password.send_keys(pixCookies.PIXPASS)
    except Exception as e:
        driver.close()
        print(e)

    try:
        driver.find_element(By.CLASS_NAME,"dMhwJU").click()
    except Exception as e:
        driver.close()
        print(e)
        
    return

#---------------------------------------------------------------------------------------------

def main():
    initDriver()
    imageURLS = getImageURLS()
    #getImages(imageURLS)
    return

main()