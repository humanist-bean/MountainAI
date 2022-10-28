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



def get_url_of_main_bing_image(driver):
    #STEP 2: get url of enlarged first image
    try:
        main_image = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="mainImageWindow"]/div[2]/div/div/div/img'))
        )
    except NoSuchElementException:
        print("Encountered a NoSuchElement expection while looking for main image " +
              str(NoSuchElementException))
    except TimeoutException:
        print("Encountered a timeout expection while looking for main image " +
              str(TimeoutException))
    finally:
        #print("Made it to finally block for main image")
        src = main_image.get_attribute('src')
        return src

#SELENIUM PART OF PROJECT WORK IN PROGRESS FROM HERE
"""
CONSTANTS    """
#DRIVER_PATH = "/home/Alder French/Desktop/RoboFarmer3000/chromedriver"
# added driver path to BASH so we don't need the above
SEARCH_PHRASES = ["mt hood", "Rainier", "mt st helens"] #for testing!
BING_IMAGE_SEARCH_STARTER = "https://www.bing.com/images/search?q="
TIME_BETWEEN_PHOTOS = 0.5 # O.2 Seconds

NUMBER_OF_PHOTOS = 5

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
    full_search = BING_IMAGE_SEARCH_STARTER + end_of_search
    print("Test: full_search is: " + full_search)
    # ABOVE CREATES URL TO SEARCH IN GOOGLE
    # NEXT SEARCH FOR THAT URL AND WAIT FOR IMAGE BUTTON
    # STEP 1. BING IMAGE SEARCH FOR URL AND CLICK ON FIRST IMAGE
    driver.get(full_search)
    try:
        img_num_one = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, "//img[contains(@alt, 'Image result for {}')]".format(phrase)))  
        ) #XPATH WORKS, By. CLASS_NAME DOESN'T!!!
    except NoSuchElementException:
        print("Encountered a NoSuchElement expection in phrase for loop: " + str(NoSuchElementException))
    except TimeoutException:
        print("Encountered a timeout expection in phrase for loop: " +
              str(TimeoutException))
    finally:
        print("Made it to finally block")
        print("OPENING THE GOOGLE IMAGES PAGE FOR: " + phrase)
        img_num_one.click()
        #TESTED AND WORKS UP TO HERE
    
    #HERE IS WHERE WE ITERATE THROUGH AND COLLECT EACH PHOTOS URL!
    #STEP 2: get url of enlarged first image NOW MOVED LOGIC TO METHOD!
    driver.switch_to.frame("{} - Bing images - details".format(phrase))
    print("Switched frames!")

    #get_url_of_main_bing_image(driver)
    
    #STEP 3. Click the "next photo" button and repeat Step 2 for
    # the number of photos you need for each mountain
    lastsrc = None
    src = None
    repeats = 0
    for i in range(0, NUMBER_OF_PHOTOS):
        big_img_next_button = WebDriverWait(driver, 7).until(
            EC.element_to_be_clickable(
                (By.ID, 'navr'))
        )
        lastsrc = src
        src = get_url_of_main_bing_image(driver)
        while(lastsrc == src):
            repeats += 1
            time.sleep(TIME_BETWEEN_PHOTOS)
            src = get_url_of_main_bing_image(driver)
        big_img_next_button.click()
        #time.sleep(5)
        print(str(i + 1) + ". image URL is: " + str(src))
        #print("MADE IT TO NEXT IMAGE!")

    print("Number of while loops because lastsrc == src: " + str(repeats))
    print("ALL DONE: exiting browser...")
    driver.quit()




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

