"""
mountain_soup.py

Description: Extracts img src tags from search engine image search pages given
a list of search phrases and downloads all the images on the webpages 
into a folder. I intend to use this program to gather many photos of mountains 
for training a mountain recognition AI. 

NOTE: this is intended for use with a virtualenv, which can be activated
by switching to the "mountainenv" directory and typing into terminal:
source bin/activate

NOTE 2: this program requires having Selenium and Chromedriver setup, with 
chromedriver added to PATH.

- by Alder French, with help from this tutorial (beautifulsoup):
https://www.makeuseof.com/python-scrape-web-images-how-to/
and this tutorial (selenium):
https://www.scrapingbee.com/blog/selenium-python/
and this tutorial (scraping from google images):
https://medium.com/geekculture/scraping-images-using-selenium-f35fab26b122

USAGE:
Given a .txt list of search phrases, one phrase per line, in terminal type:
./mountain_soup.py path/to/search/phrase_list.txt

"""

from logging import exception
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException





#SELENIUM PART OF PROJECT WORK IN PROGRESS FROM HERE
"""
CONSTANTS    """
#DRIVER_PATH = "/home/Alder French/Desktop/RoboFarmer3000/chromedriver"
# added driver path to BASH so we don't need the above
GOOG_IMG_BTN_CLASS_CODE = "cDaxAd"
SEARCH_PHRASES = ["mt hood", "Rainier", "mt st helens"] #for testing!
GOOGLE_SEARCH_STARTER = "https://www.google.com/search?q="

""" SELENIUM TEST - (WORKS)
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

service = Service(DRIVER_PATH)
#service.start()
#driver = webdriver.Remote(service.service_url)
#driver = webdriver.Chrome(DRIVER_PATH, options=options)
driver = webdriver.Chrome() #THIS WORKS! YAY GOT SELENIUM WORKING!


driver.get("https://www.nintendo.com/")
time.sleep(5)
print(driver.page_source)
driver.quit() END TEST"""

'''GET SEARCH PHRASES FROM .TXT LIST, THEN LOOP THROUGH EACH ONE DOING:
1. Get the google search page for that phrase
2. Click on the "Images" button to go to the images search results page
3. Start collecting the URLs of the images, try to get the URLs to
the full size images, not the little previews that show up on the search
page itself. NOTE: you can prevent selenium from actually loading all the
photos to speed up the collection of image URLs, see the 
"blocking javascript and images" part of scraping bee's selenium tutorial.
We can finally download the images at the end of this process by writing 
image URLs directly into a folder in our computer, initiating the computer
systems automatic downloading process so our code can keep running fast.
4. Scroll down the page till selenium sees googles show more results button
via something like: 
try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.Value, "Show more results"))
    )
finally:
    driver.quit()
5. Repeat steps 3 and 4 till the required number of 
photos for that term is collected OR
there are no more photos to download. Make sure to test for no more photos
and gracefully exit the search for that term.
6. Repeat steps 1 - 6 for each search phrase by using the for loop. 

'''
search_phrases = ["mt hood"] #SEARCH_PHRASES
driver = webdriver.Chrome()  # THIS WORKS! YAY GOT SELENIUM WORKING!
for phrase in search_phrases:
    words = phrase.split()
    if len(words) <= 0:
        print("WARNING: The length of this phrase is <= 0: " + phrase)
        continue
    end_of_search = words[0]
    for word in words[1:]:
        end_of_search  = end_of_search + "+" + word
    full_search = GOOGLE_SEARCH_STARTER + end_of_search
    print("Test: full_search is: " + full_search)
    # ABOVE CREATES URL TO SEARCH IN GOOGLE
    # NEXT SEARCH FOR THAT URL AND WAIT FOR IMAGE BUTTON
    driver.get(full_search)
    try:
        goog_img_btn = WebDriverWait(driver, 7).until(
            #EC.element_to_be_clickable((By.CLASS_NAME, "jmeM8b"))
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[7]/div/div[4]/div/div[1]/div/div[1]/div/div[2]/a"))
        ) #XPATH WORKS, By. CLASS_NAME DOESN'T!!!
    except NoSuchElementException:
        print("Encountered a NoSuchElement expection in phrase for loop: " + str(NoSuchElementException))
    except TimeoutException:
        print("Encountered a timeout expection in phrase for loop: " +
              str(TimeoutException))
    else:
        print("OPENING THE GOOGLE IMAGES PAGE FOR: " + phrase)
        goog_img_btn.click()
        time.sleep(7) 
    finally:
        print("Made it to finally block")
        #driver.quit()





 #TO HERE END SELENIUM WORK IN PROGRESS


""" BEGIN BeautifulSoup TEST (WORKS)
NOTE: What I have below is a good start especially for resolving
weird URLs and downloading images from URLs to folders, but I will need to
install and use SELENIUM to scrape data without using an expensive API.


URL = "https://www.google.com/search?q=grand+tetons&tbm=isch&sxsrf=ALiCzsYGUyL81tfzBDq7Hgjxd4bTE_MdHQ%3A1666680807354&source=hp&biw=1280&bih=603&ei=54dXY9CaE8yD0PEP__WLYA&iflsig=AJiK0e8AAAAAY1eV9wFlyi6QfUQr22Lg_wD3pe-Omr3T&ved=0ahUKEwiQquXr5fr6AhXMATQIHf_6AgwQ4dUDCAY&uact=5&oq=grand+tetons&gs_lcp=CgNpbWcQAzIECCMQJzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoHCCMQ6gIQJzoICAAQsQMQgwE6CAgAEIAEELEDOgsIABCABBCxAxCDAVC6FFjyLGC6LmgDcAB4AIABZIgBvAeSAQQxMy4xmAEAoAEBqgELZ3dzLXdpei1pbWewAQo&sclient=img#imgrc=Z51xKzTA1MX3sM" #Paste URL here

getURL = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"})

soup = BeautifulSoup(getURL.text, 'html.parser')

images = soup.find_all('img')

resolvedURLs = []
for image in images:
    src = image.get('src')
    resolvedURLs.append(requests.compat.urljoin(URL, src))

for image in resolvedURLs:
    webs = requests.get(image)
    open('images/test_images_00/' + image.split('/')[-1], 'wb').write(webs.content)

print("SUCCESSFULLY SCRAPED PHOTOS!")
#STOPPED HERE 10/25/2022 TESTED AND WORKING SO FAR!

END BEAUTIFUL SOUP TEST"""

