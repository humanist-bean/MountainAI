"""
mountain_list_cleaner.py
by Alder French

Usage:
python3 mountain_list_cleaner.py infile.txt outfile.txt

Description:
Takes a .txt file with one mountain name per line as input and if the mountain
name does not already contain "mountain", "mt.", "mt", "mount", "butte",
or "peak", this program appends "mountain" to the end of the name so that we
don't get silly photos instead of photos of the mountain when scraping the web
for photos in mountain_soup.py.
"""

import sys
import re


def clean_list(input_name, output_name):
    mountain_list_dirty = open(input_name, "r", encoding="utf-8")
    mountain_list_clean = open(output_name, "w")
    mountain_words = ['mountain', 'mt.', 'mt', 'mount', 'butte', 'peak']
    for line in mountain_list_dirty.readlines():
        line = line.lower()
        line = re.sub('[^A-Za-z0-9]+', ' ', line) #removes all non number or letter characters
        mt_names = 0
        for word in mountain_words:
            if word in line:
                mt_names += 1
        if mt_names == 0:
            line = line.strip()
            line = line + ' mountain \n'
        else:
            line = line + '\n'
        #print(line)
        mountain_list_clean.write(line)
    mountain_list_dirty.close()
    mountain_list_clean.close()



if __name__ == "__main__":
    print("Running mountain_list_cleaner.py...")
    # CONSTANTS
    # print(len(sys.argv))
    if len(sys.argv) > 1:
        input_text_file = str(sys.argv[1])
        output_text_file = str(sys.argv[2])
    else:
        input_text_file = str(input("Enter the name of the .txt file where your list of mountains is. \n"))
        output_text_file = str(input("Enter the name you want for your output file ending in .txt .\n"))
    clean_list(input_text_file, output_text_file)
