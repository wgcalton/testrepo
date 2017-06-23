##### img-grbbr.py ####
# Author: Will Calton #
#     June 2017       #
#######################

import csv
import random
import time

import mechanicalsoup
from bs4 import BeautifulSoup


'''--- Functions ---'''

#Pulls ASIN data from csv
def getASIN():
    with open('VG-ASINS.csv') as csvfile:
        rdr = csv.DictReader(csvfile)
        for row in rdr:
            asins = row['ASIN']
            yield asins

#Pull Description data from csv
def getDesc():
    with open('VG-ASINS.csv') as csvfile:
        rdr = csv.DictReader(csvfile)
        for row in rdr:
            desc = row['Description']
            yield desc

#Pulls webpage data and saves image
def getIMG(asin):
    browser = mechanicalsoup.StatefulBrowser(soup_config={'features':'lxml'})
    page = (
        browser.get('http://www.amazon.com/dp/' + asin,
                    headers={'referer': 'https://www.amazon.com'})
        )

    soup = page.soup
    try:
        imgsrc = soup.find('img', id='landingImage').get('src')
        return imgsrc
    except AttributeError:
        imgsrc = (
            soup.find('div', _class='imgTagWrapper')
            .findNext('img').get('src')
            )
        

#Retrieves image source and saves image
def saveIMG(imgsrc, filename):
    browser = mechanicalsoup.StatefulBrowser(soup_config={'features':'lxml'})
    page = (
        browser.get(imgsrc, 
                    headers={'referer': 'https://www.amazon.com'})
        )
    with open('imgs/' + str(filename), 'wb') as f:
        f.write(page.content)
        f.close()
    
#Assigning csv data to global variables
global asins, filename

asins = list(getASIN())
filename = list(getDesc())

#Main Loop:  Loops through each row in csv
count = len(asins)
for i in range(count)[396:]:
    if asins[i] == '':
        pass
    else:
        print(i)
        try:
            imgsrc = getIMG(asins[i])
            time.sleep(random.randint(1,15))
            saveIMG(imgsrc, filename[i])
            time.sleep(random.randint(1,10))
        except AttributeError as e:
            try:
                time.sleep(random.randint(1,15))
                imgsrc = getIMG(asins[i])
                time.sleep(random.randint(1,15))
                saveIMG(imgsrc, filename[i])
                time.sleep(random.randint(1,10))
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

