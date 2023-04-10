from itertools import zip_longest
from itertools import chain
import re
import time
from datetime import datetime
from urllib.parse import parse_qs, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import csv
import json

options = webdriver.ChromeOptions()

options.add_argument('headless')

driver = webdriver.Chrome(options=options)

totalData = {}

def writeJson(data):
    with open('json/scrapedPages'+ '' + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def writeCSV(driver,data):   
    data['hours'].insert(0, 'days')
    with open('scraps/'+driver.title + '.csv', 'w', encoding='utf-8') as csvfile:
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
                        row.append((hour, ''))
                writer.writerow(dict(row))


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
                
def sortHours(arrayToSort):
    arrayToSort = [datetime.strptime(date,'%H:%M') for date in arrayToSort]
    arrayToSort.sort()
    sortedArray =  [date.strftime('%H:%M') for date in arrayToSort]
    return sortedArray


def formatHour(hour):
    hour = hour.strip()
    hour = hour.replace('\u202f', ':00 ')
    date = datetime.strptime(hour,'%I:%M %p')
    hour = date.strftime('%H:%M')
    return hour

def getMetaData(driver, url):
    latitude = re.search("!3d([0-9a-zA-Z.]+)!?", url).group(1)
    longitude = re.search("!4d([0-9a-zA-Z.]+)!?", url).group(1)
    title = driver.title.split(' - ')[0]
    metaData = {
        'coordinates': {
            'latitude': latitude,
            'longitude': longitude
        },
        'title': title
    }
    return metaData
def scrapeWebsite(url):
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
    # bypass cookies
    try:
        cookiesDecliner = WebDriverWait(driver, timeout=2).until(lambda b: b.find_element(By.XPATH,"//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe']"))
        cookiesDecliner.click()
    except:
        pass
    print(driver.title)
    print(getMetaData(driver, url))
    scrapedData['metaData'].update(getMetaData(driver,url))

    el = WebDriverWait(driver, timeout=10).until(lambda b: b.find_element(By.CLASS_NAME,"dpoVLd"))
    elements = driver.find_elements(By.CLASS_NAME,"dpoVLd")
    
    for element in elements:
        try:
            day = getDay(element.find_element(By.XPATH,"./../..").get_attribute("jsinstance"))
            text    = element.get_attribute('aria-label')
            percentage = text.split('%')[0]
            # print(text)
            if 'at' in text.split('%')[1][-6:-1]:
                continue
            if 'Currently' in text:
                hour = datetime.now().strftime("%H:00")
                percentage = text.split('%')[1][-2:]
            else:
                hour = formatHour(text.split('%')[1][-6:-1])
            if hour not in scrapedData['peakHours']['hours']:
                scrapedData['peakHours']['hours'].append(hour) 
            scrapedData['peakHours'][''+day].append((hour,percentage))
        except Exception as e:
            print (e)
            continue
    scrapedData['peakHours']['hours'] = sortHours(scrapedData['peakHours']['hours'])
    # writeCSV(driver, scrapedData['peakHours'])
    # totalData[''+driver.title] = scrapedData
    return driver.title.split(' - ')[0], scrapedData

sites = []
def getLinks(query):
    url = 'https://www.google.com/maps/search/' + query + '/'
    driver.get(url)
    try:
        cookiesDecliner = WebDriverWait(driver, timeout=2).until(lambda b: b.find_element(By.XPATH,"//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe']"))
        cookiesDecliner.click()
    except:
        pass
    # resultPanel = WebDriverWait(driver, timeout=2).until(lambda b: b.find_element(By.XPATH,"//div[@class='m6QErb DxyBCb kA9KIf dS8AEf ecceSd']"))
    for i in range(5):
        try:
            element = WebDriverWait(driver, timeout=3).until(lambda b: b.find_element(By.XPATH,"(//a[@class='hfpxzc'])[last()]"))
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
        except:
            pass
    links = driver.find_elements(By.XPATH,"//a[@class='hfpxzc']")
    for link in links:    
        sites.append(link.get_attribute('href'))
        
getLinks('restaurant koblenz')

# sites = ['https://www.google.be/maps/place/Catberry/@51.0410502,3.7226083,15z/data=!4m10!1m2!2m1!1scatberry+gent!3m6!1s0x47c371395c187645:0x69ed7cc1afaf942a!8m2!3d51.0487767!4d3.7341216!15sCg1jYXRiZXJyeSBnZW50Wg8iDWNhdGJlcnJ5IGdlbnSSAQtjb2ZmZWVfc2hvcOABAA!16s%2Fg%2F11tjld_963', 'https://maps.app.goo.gl/cGkpKnhaLvrafbBLA', 'https://maps.app.goo.gl/gfPtMmFhi1QoVprFA']
# sites = ['https://www.google.be/maps/place/Catberry/@51.0410502,3.7226083,15z/data=!4m10!1m2!2m1!1scatberry+gent!3m6!1s0x47c371395c187645:0x69ed7cc1afaf942a!8m2!3d51.0487767!4d3.7341216!15sCg1jYXRiZXJyeSBnZW50Wg8iDWNhdGJlcnJ5IGdlbnSSAQtjb2ZmZWVfc2hvcOABAA!16s%2Fg%2F11tjld_963', ]
for site in sites:
    try:
        title, data = scrapeWebsite(site)
        totalData[''+title] = data
        print('Done with' + title)
    except Exception as e:
        print(e)
        pass
writeJson(totalData)