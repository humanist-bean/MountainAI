#Note: This code was shamelessly copied from stack overflow
from bs4 import BeautifulSoup
import requests

url = "https://en.wikipedia.org/wiki/List_of_mountains_by_elevation"

res = requests.get(url)
soup = BeautifulSoup(res.text,"lxml")

#testing
i = 0
for table in soup.find_all(class_="wikitable"):
    #print(str(i))
    #i+=1
    for items in table.find_all("tr")[1:]:
        e = items.find_all('td')
        data = f'{e[0].text.strip()}'
        print(data)

'''
for items in soup.find(class_="wikitable").find_all("tr")[1:]:
    e = items.find_all('td')
    data = f'{e[0].text.strip()}'
    print(data)
'''