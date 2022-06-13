
import requests
from bs4 import BeautifulSoup
import pixCookies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from os import path

wdOptions = webdriver.ChromeOptions()
wdOptions.add_argument('--ignore-certificate-errors')
wdOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
#wdOptions.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=wdOptions)

cookies = pixCookies.COOKIES
headers = pixCookies.HEADERS
imageLimit = 3
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
        getImageFromURL(urlBase + urlSuffix)
        return
       
def getImageFromURL(URL):
    #print("navigating to url: " + URL)
    sleep(5)
    driver.get(URL)
    try:
        img = WebDriverWait(driver,timeout=5).until(lambda d: d.find_element(By.CLASS_NAME,"gtm-expand-full-size-illust"))
        imgURL = img.get_attribute("href")
    except Exception as e:
        driver.close()
        print("Cannot find element" + e)


    filepath = path.join("C:/Users/arrot/Desktop/sImages/",imgURL[-15:-1])
    imgheaders = {'referer': 'https://www.pixiv.net/en/'}

    img_data = requests.get(imgURL,headers=imgheaders)


    with open(filepath,'wb') as handler:
        handler.write(img_data.content)

    #sleep(5)
    driver.close()

    return

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
        password = driver.find_element(By.CLASS_NAME,"hfoSmp")
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
    getImages(imageURLS)
    print("downloads complete")
    return

main()