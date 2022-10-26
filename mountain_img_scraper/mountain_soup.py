"""
mountain_soup.py

Description: Extracts img src tags from search engine image search pages given
a list of search phrases and downloads all the images on the webpages 
into a folder. I intend to use this program to gather many photos of mountains 
for training a mountain recognition AI. 

NOTE: this is intended for use with a virtualenv, which can be activated
by switching to the "mountainenv" directory and typing into terminal:
source bin/activate

- by Alder French, with help from this tutorial:
https://www.makeuseof.com/python-scrape-web-images-how-to/

USAGE:
Given a .txt list of search phrases, one phrase per line, in terminal type:
./mountain_soup.py path/to/search/phrase_list.txt

"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



#SELENIUM PART OF PROJECT WORK IN PROGRESS FROM HERE
"""
CONSTANTS    """
DRIVER_PATH = '~/Desktop/RoboFarmer3000/chromedriver'
GOOG_IMG_BTN_CLASS_CODE = 'cDaxAd'

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

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
for search in search_phrases:
    driver.get('https://google.com')




 #TO HERE END SELENIUM WORK IN PROGRESS


"""NOTE: What I have below is a good start especially for resolving
weird URLs and downloading images from URLs to folders, but I will need to
install and use SELENIUM to scrape data without using an expensive API.
"""

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


