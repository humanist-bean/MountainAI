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


