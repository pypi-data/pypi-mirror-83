import pandas as pd
import geopy
import geopy.distance
from bs4 import BeautifulSoup
import json
import requests
import logging
import re
import datetime


_LOGGER = logging.getLogger(__name__)

MS_BASE_URL = 'https://www.meteosuisse.admin.ch'
MS_SEARCH_URL = 'https://www.meteosuisse.admin.ch/home/actualite/infos.html?ort={}&pageIndex=0&tab=search_tab'
CURRENT_CONDITION_URL= 'https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv'
STATION_URL = "https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/info/VQHA80_fr.txt"
MS_24FORECAST_REF = "https://www.meteosuisse.admin.ch//content/meteoswiss/fr/home.mobile.meteo-products--overview.html"
MS_24FORECAST_URL = "https://www.meteosuisse.admin.ch/product/output/forecast-chart/{}/fr/{}00.json"
_LOGGER.debug("Start update 24h forecast data")
s = requests.Session()
#Forcing headers to avoid 500 error when downloading file
s.headers.update({"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})
searchUrl = MS_SEARCH_URL
_LOGGER.debug("Main URL : %s"%searchUrl)
tmpSearch = s.get(MS_24FORECAST_REF,timeout=10)
s.get("https://www.meteosuisse.admin.ch/etc/designs/meteoswiss/ajax/location/123300.json")
soup = BeautifulSoup(tmpSearch.text,features="html.parser")
widgetHtml = soup.find_all("div",{"class": "overview__local-forecast"})
jsonUrl = widgetHtml[0].get("data-json-url")
jsonUrl = str(jsonUrl)
version = jsonUrl.split('/')[4]
forecastUrl = MS_24FORECAST_URL.format(version,"1233")
_LOGGER.debug("Data URL : %s"%forecastUrl)
s.headers.update({'referer': MS_24FORECAST_REF,"x-requested-with": "XMLHttpRequest","Accept": "application/json, text/javascript, */*; q=0.01","dnt": "1"})
jsonData = s.get(forecastUrl,timeout=10)
jsonData.encoding = "utf8"
jsonDataTxt = jsonData.text

jsonObj = json.loads(jsonDataTxt)
print(jsonObj)

done= False

class hourData(object):
    pass

while(not done):
    curDate = datetime.datetime.fromtimestamp(int(str(jsonObj[0]['current_time'])[0:-3]))
    curHour = curDate.hour
    for i in range(1,24):
        nextHour = hourData() 
        nextHour.hour = curHour + i % 24  
        print(nextHour)
    done = True