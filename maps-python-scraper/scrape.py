from itertools import zip_longest
from itertools import chain
import re
import time
from datetime import datetime
from urllib.parse import parse_qs, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# from main import driver
import csv
import json

def writeJson(data):
    with open('json/scrapedPages'+ '' + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def writeCSV(title,data):   
    data['hours'].insert(0, 'days')
    with open('scraps/'+title + '.csv', 'w', encoding='utf-8') as csvfile:
            fieldnames = list(data['hours'])
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for day in list(data)[1:]:
                row = []
                row.append(('days',day))
                for hour in data['hours'][1:]:
                    try: 
                        row.append((hour, dict(data[day])[''+hour]))
                    except KeyError:
                        print(KeyError)
                        row.append((hour, ''))
                writer.writerow(dict(row))

# Function to get day based on number
def getDay(num):
    switch={
        '1':'Monday',
        '2':'Tuesday',
        '3':'Wednesday',
        '4':'Thursday',
        '5':'Friday',
        '6':'Saturday',
        '0':'Sunday',
        '*1':'Monday',
        '*2':'Tuesday',
        '*3':'Wednesday',
        '*4':'Thursday',
        '*5':'Friday',
        '*6':'Saturday',
        '*0':'Sunday'
      }
    return switch.get(num,"Invalid input")

# sort hours 
def sortHours(arrayToSort):
    arrayToSort = [datetime.strptime(date,'%H:%M') for date in arrayToSort]
    arrayToSort.sort()
    sortedArray =  [date.strftime('%H:%M') for date in arrayToSort]
    return sortedArray

# convert string from scrape to datetime
def convertHourToDateTime(hour):
    hour = hour.strip()
    hour = hour.replace('\u202f', ':00 ')
    date = datetime.strptime(hour,'%I:%M %p')
    hour = date.strftime('%H:%M')
    return hour

# get meta data from url
def getMetaDataFromUrl(driver, url):
    latitude = re.search("!3d([0-9a-zA-Z.]+)!?", url).group(1)
    longitude = re.search("!4d([0-9a-zA-Z.]+)!?", url).group(1)
    title = driver.title.split(' - ')[0]
    metaData = {
        'coordinates': {
            'latitude': latitude,
            'longitude': longitude
        },
        'title': title,
        'url': url	
    }
    return metaData

def scrapeWebsite(driver, url):
    # instanciate data array
    scrapedData = {
        'peakHours':{
        'hours':[],
        'Monday':[],
        'Tuesday':[],
        'Wednesday':[],
        'Thursday':[],
        'Friday':[],
        'Saturday':[],
        'Sunday':[],
        },
        'metaData':{
        }
    }
    driver.get(url)
    print(driver.title)
		# wait for elements of rush hours to load
		# these are the bars of the rush hour table
    WebDriverWait(driver, timeout=1).until(lambda b: b.find_element(By.CLASS_NAME,"dpoVLd"))
    chartBars = driver.find_elements(By.CLASS_NAME,"dpoVLd")
    # rewrite to start with aprent element
    for chartBar in chartBars:
        try:
            # get parent element of the beam
            day = getDay(chartBar.find_element(By.XPATH,"./../..").get_attribute("jsinstance"))
            text    = chartBar.get_attribute('aria-label')
            percentage = text.split('%')[0]
            # print(text)
            if 'at' in text.split('%')[1][-6:-1]:
                continue
            if 'Currently' in text:
                hour = datetime.now().strftime("%H:00")
                percentage = text.split('%')[1][-2:]
            else:
                hour = convertHourToDateTime(text.split('%')[1][-6:-1])
            if hour not in scrapedData['peakHours']['hours']:
                scrapedData['peakHours']['hours'].append(hour) 
            scrapedData['peakHours'][''+day].append((hour,percentage))
        except Exception as e:
            print (e)
            continue
    scrapedData['peakHours']['hours'] = sortHours(scrapedData['peakHours']['hours'])
    scrapedData['metaData'].update(getMetaDataFromUrl(driver,url))
    scrapedData['metaData']['scrapedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    scrapedData['metaData'].update({
				'scrapedAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'address': driver.find_element(By.CLASS_NAME,"Io6YTe").text,
		})
    return scrapedData['metaData']['title'], scrapedData


def getLinks(driver, query, amount = 1):
    sites = []
    url = 'https://www.google.com/maps/search/' + query + '/'
    driver.get(url)
    while len(driver.find_elements(By.CLASS_NAME,"hfpxzc")) < amount:
        try:
            element = WebDriverWait(driver, timeout=2).until(lambda b: b.find_element(By.XPATH,"(//a[@class='hfpxzc'])[last()]"))
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
        except Exception as e:
            print(e)
            pass
    links = driver.find_elements(By.CLASS_NAME,"hfpxzc")
    for link in links:    
        sites.append(link.get_attribute('href'))
    print(len(sites))
    return sites
        
def scrapeDataFromLinks(driver, links, amount = 1):
		totalData = {}
		for link in links[:amount]:
			try:
					title, data = scrapeWebsite(driver, link)
					totalData[''+title] = data
					print('Done with ' + title)
			except Exception as e:
					print(e)
					pass
		# driver.close() 
		return totalData


def main(driver, query, amount = 1):
	links = getLinks(driver, query, amount)
	data = scrapeDataFromLinks(driver, links, amount)
	return data
