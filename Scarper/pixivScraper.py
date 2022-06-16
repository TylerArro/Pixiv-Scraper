
import requests
from bs4 import BeautifulSoup
import pixCookies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from os import path

#from webdriver_manager.chrome import ChromeDriverManager
#driver = webdriver.Chrome(ChromeDriverManager().install(), options=wdOptions)

wdOptions = webdriver.ChromeOptions()
wdOptions.add_argument('--ignore-certificate-errors')
wdOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
wdOptions.add_argument('--headless')

driver = webdriver.Chrome('chromedriver', options=wdOptions)

cookies = pixCookies.COOKIES
headers = pixCookies.HEADERS
urlBase = "https://www.pixiv.net"

#-------------------FUNCTIONS-------------------------------------------------------------------
#get image html elements that contain image urls using BS4
#parameter: amount of images to scrape
def getRankingImageURLS(imageLimit=10):
    response = requests.get('https://www.pixiv.net/ranking.php', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup.prettify())

    imageHTML = soup.find_all("a",class_="work _work",limit=imageLimit)
    return imageHTML

#get image urls from pixiv user profile using pixiv ID using Selenium + BeautifulSoup
def getUserImageURLS(imageLimit,userID):
    imgURLS = []
    sleep(3)
    #print(urlBase + "/en/users/" + str(userID))
    driver.get(urlBase + "/en/users/" + str(userID))

    try:
        imgDivs = WebDriverWait(driver,timeout=5).until(lambda d: d.find_elements(By.CLASS_NAME,'fGjAxR'))
        for x in range(imageLimit):
            imgURLS.append(imgDivs[x].get_attribute("href"))
    except Exception as e:
        driver.close()
        print("Cannot find element")

    return imgURLS

    
#extract the URLs from the html elements list
def getImages(ImagesUrls,rankings):
    if rankings == True:
        for x in ImagesUrls:
            urlSuffix = x.attrs['href']
            print(urlBase + urlSuffix)
            getImageFromURL(urlBase + urlSuffix)
    else:
        for url in ImagesUrls:
            getImageFromURL(url)
    return

# navigate the driver to pixiv illustration page, get actaul image url and download it
def getImageFromURL(URL):
    sleep(3)
    driver.get(URL)
    print(URL)
    try:
        img = WebDriverWait(driver,timeout=5).until(lambda d: d.find_element(By.CLASS_NAME,"gtm-expand-full-size-illust"))
        imgURL = img.get_attribute("href")
        print(imgURL)
    except Exception as e:
        driver.close()
        print("Cannot find element")
        print(e)


    filepath = path.join("C:/Users/arrot/Desktop/sImages/",imgURL[-15:])
    imgheaders = {'referer': 'https://www.pixiv.net/en/'}

    img_data = requests.get(imgURL,headers=imgheaders)


    with open(filepath,'wb') as handler:
        handler.write(img_data.content)

    return

#initialize selenium driver to login to pixiv 

def initDriver():
    #go to pixiv site
    driver.get(urlBase)
    #find login button and click it
    driver.find_element(By.CLASS_NAME,'signup-form__submit--login').click()

    #find username and password fields and fill them in
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

    print("driver Logged into pixiv")

    return

#---------------------------------------------------------------------------------------------
# base function to scrape rankings 
def scrapeRankings(amount):
    #login to pixiv with selenium driver 
    initDriver()

    #get image urls from pixiv using BeautifulSoup
    imageURLS = getRankingImageURLS(amount)

    #get images from image urls
    getImages(imageURLS,True)
    print("downloads complete")

    #close chromedriver
    driver.close()
    return

def scrapeUser(amount,userID):
    #login to pixiv with selenium driver 
    initDriver()

    #get amount image urls from pixiv user profile using pixiv ID using beatufisoup
    imageURLS = getUserImageURLS(amount,userID)
    
    #get images from image urls
    getImages(imageURLS,False)
    print("downloads complete")

    #close chromedriver
    driver.close()
    return
#---------------------------------------------------------------------------------------------

driver.quit()
scrapeRankings(3)
#scrapeUser(3,2356928)
driver.quit()
#TODO - add a function to scrape by tag and by user