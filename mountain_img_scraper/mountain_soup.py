"""
mountain_soup.py

Description: Extracts img src tags from search engine image search pages given
a list of search phrases and downloads all the images on the webpages 
into a folder. I intend to use this program to gather many photos of mountains 
for training a mountain recognition AI. 

COMMANDS
Example (this is tested and works given the folder test_images_01 already exists):
"sudo python mountain_soup.py test_mountains_small.txt images/test_images_01/ 7"

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
import sys
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException


def txt_to_phrase_list(txtFileString):
    """
    INPUT: a string that references a .txt file with 1 search phrase per line,
     e.g. "somewords.txt"

    OUTPUT: a list where each element is a phrase from a line of the .txt file
    """
    phrase_list = []
    with open(txtFileString) as file:
        for line in file:
            phrase_list.append(line.rstrip())
    return phrase_list
            

def get_url_of_main_bing_image(driver):
    #STEP 2: get url of enlarged first image
    try:
        main_image = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="mainImageWindow"]/div[2]/div/div/div/img'))
        )
    except NoSuchElementException:
        print("Encountered a NoSuchElement expection while looking for main image: " +
              str(NoSuchElementException))
    except TimeoutException:
        print("Encountered a timeout expection while looking for main image: " +
              str(TimeoutException))
    else:
        #print("Made it to finally block for main image")
        try:
            src = main_image.get_attribute('src')
        except StaleElementReferenceException:
            print("Encountered a stale element reference exception while looking for main image's src: " +
                  str(StaleElementReferenceException))
            time.sleep(1)
            return get_url_of_main_bing_image(driver) # upon this exception retry method via recursive call
        return src


# change to accept list of search phrases!
def get_image_sources(search_phrase_list, number_of_photos_per_phrase):
    #SELENIUM PART OF PROJECT WORK IN PROGRESS FROM HERE
    """
    NOTE: you can prevent selenium from actually loading all the
    photos to speed up the collection of image URLs, see the 
    "blocking javascript and images" part of scraping bee's selenium tutorial.
    """
    #CONSTANTS
    BING_IMAGE_SEARCH_STARTER = "https://www.bing.com/images/search?q="
    TIME_BETWEEN_PHOTOS = 1.0 # in Seconds
    TRIES = 3

    # SELENIUM AND CHROMEDRIVER SETTINGS
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    ### This blocks images and javascript requests which speeds up
    ### image collection but also makes it so we only collect URLs
    ### of the lower quality images, which might be ok...
    """
    chrome_prefs = {
        "profile.default_content_setting_values": {
            "images": 2,
        }
    }
    chrome_options.experimental_options["prefs"] = chrome_prefs
    """
    ###

    search_phrases = search_phrase_list #["mt hood"] #SEARCH_PHRASES
    # THIS WORKS! YAY GOT SELENIUM WORKING!
    driver = webdriver.Chrome(options=chrome_options)
    sources = []
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
        print("OPENING THE GOOGLE IMAGES PAGE FOR: " + phrase)
        success = False
        for x in range (1, TRIES):
            try:
                driver.get(full_search)
                img_num_one = WebDriverWait(driver, 7).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//img[contains(@alt, 'Image result for {}')]".format(phrase)))
                ) #XPATH WORKS, By. CLASS_NAME DOESN'T!!!
                img_num_one.click()
                success = True
                break
            except NoSuchElementException:
                print("Encountered a NoSuchElement exception in phrase for loop: " + str(NoSuchElementException))
                time.sleep(1)
                continue
            except TimeoutException:
                print("Encountered a timeout exception in phrase for loop: " +
                    str(TimeoutException))
                time.sleep(1)
                continue
            except WebDriverException:
                print("Encountered a Web Driver exception in phrase for loop: " +
                      str(TimeoutException))
                time.sleep(1)
                continue
            except StaleElementReferenceException:
                print("Encountered a stale element reference exception while attempting to click on the first image: " +
                      str(StaleElementReferenceException))
                time.sleep(1)
                continue
        if not success:
            print("Failed to open page for: " + phrase + ", filling sources with None and continuing to next phrase...")
            for y in range(0, number_of_photos_per_phrase):
                sources.append(None)  # fill remaining sources positions with None
            driver.quit()
            return sources

        #TESTED AND WORKS UP TO HERE
        
        #HERE IS WHERE WE ITERATE THROUGH AND COLLECT EACH PHOTOS URL!
        #STEP 2: get url of enlarged first image NOW MOVED LOGIC TO METHOD!
        driver.switch_to.frame("{} - Bing images - details".format(phrase))
        print("Switched frames!")
        
        #STEP 3. Click the "next photo" button and repeat Step 2 for
        # the number of photos you need for each mountain
        lastsrc = None
        src = None
        for i in range(0, number_of_photos_per_phrase):
            lastsrc = src
            src = get_url_of_main_bing_image(driver)
            repeats = 0
            while(lastsrc == src) and repeats < 7:
                repeats += 1
                time.sleep(TIME_BETWEEN_PHOTOS * (repeats + 1))
                src = get_url_of_main_bing_image(driver)         
            print(str(i + 1) + ". image URL is: " + str(src))
            sources.append(src)
            for k in range(0, TRIES):  #try TRIES times then skip cuz probably no more photos and thus no button
                try:
                    big_img_next_button = WebDriverWait(driver, 7).until(
                        EC.presence_of_element_located(
                            (By.ID, 'navr'))
                    )
                    big_img_next_button.click()
                    break
                except StaleElementReferenceException:
                    print("Encountered a stale element reference exception while attempting to click big image's next button" +
                          str(StaleElementReferenceException))
                    time.sleep(1)
                except NoSuchElementException:
                    print("Encountered a NoSuchElement expection in NESTED next image button grab: " +
                          str(NoSuchElementException))
                except TimeoutException:
                    print("Encountered a timeout expection in NESTED next image button grab: " +
                          str(TimeoutException))
            if k >= (TRIES - 1): #runs when there is no more next image button because there is no more images
                print("Tried to grab button " + str(TRIES) + " times, skipping because we probably just ran out of photos"
                       + " for this bing image search")
                for j in range((i + 1), number_of_photos_per_phrase):
                    sources.append(None) #fill remaining sources positions with None
                break
            #print("MADE IT TO NEXT IMAGE!")

        print("Number of while loops because lastsrc == src: " + str(repeats))
        print("Done collecting image URLs: exiting browser...")

    driver.quit()
    return sources
    #TO HERE END SELENIUM WORK IN PROGRESS


def urls_to_images_in_folder(urls, path_to_images_folder, search_phrase_list, number_of_each):
    """
    INPUT: a python list of urls from get_imageg_sources(), and a string that
    is a path to the folder where the user wants their images to go.
    NOTE: this folder needs to exist before running mountain_soup.py!

    OUTPUT: returns nothing but stores photos in folder. 
    """
    #parent_dir = "~/Desktop/MountainAI/mountain_img_scraper/"
    parent_dir_less_slash = "~/Desktop/MountainAI/mountain_img_scraper"
    k = 0
    for phrase in search_phrase_list:
        folder_path = path_to_images_folder
        for i in range(0, number_of_each):
            image = urls[i + (k * number_of_each)]
            if image != None:
                webs = requests.get(image)
                open(folder_path + phrase + " " + str(i), 'wb').write(webs.content)
        k += 1



if __name__ == "__main__":
   print("Running mountain_soup.py...")
   #CONSTANTS
   #print(len(sys.argv))
   if len(sys.argv) > 1:
       phrase_text_file = str(sys.argv[1])
       image_folder_path = str(sys.argv[2])
       number_of_photos = int(sys.argv[3])
   else:
        phrase_text_file = str(input("Enter the name of the .txt file where your search phrases are. \n"))
        image_folder_path = str(input("Enter the path to your image downloads folder starting without '/' but ending with '/'.\n"))
        number_of_photos = int(input("Enter the number of photos you want for each search phrase.\n"))
   SEARCH_PHRASES = ["mt hood", "Rainier", "mt st helens"]  # for testing!
   NUMBER_OF_PHOTOS = 5
   search_phrases = txt_to_phrase_list(phrase_text_file)
   urls = get_image_sources(search_phrases, number_of_photos)
   urls_to_images_in_folder(urls, image_folder_path, search_phrases, number_of_photos)
   print("FINISHED: mountain_soup.py is done running...")
