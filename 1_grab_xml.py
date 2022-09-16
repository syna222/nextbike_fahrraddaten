from bs4 import BeautifulSoup
from datetime import datetime
import lxml
from lxml import etree
import os
import requests
import schedule
import time

## --- GRABS XML FROM COLOGNE'S NEXTBIKE-API EVERY HOUR (UNTIL SET END TIME) AND SAVES IT AS TIMESTAMPED XML --- ##

city_codes = {"Augsburg":178,
              "Berlin":362, "Bielefeld":16, "Bonn":547, "Bremen":379,
              "Dresden":685, "Düsseldorf":50,
              "Erfurt":493,
              "Frankfurt":8, "Freiburg":619,
              "Hannover":87, "Heidelberg":194,
              "Kaiserslautern":398, "Karlsruhe":21, "Kiel":613, "Köln":14,
              "Leipzig":1, 
              "Mannheim":195,
              "Nürnberg":626,
              "Potsdam":158,
              "Wiesbaden":7, "Würzburg":281}

def get_times():
    #get current time:
    now = datetime.now()
    current_time = now.strftime("%d/%m/%y/%H:%M:%S") 
    filename_part = now.strftime("%d%m%y%H%M%S")
    return current_time, filename_part

def get_xml(city_name):
    #get times:
    current_time, filename_part = get_times()
    #create tag for metadata:
    tag = "<metadata><datetime>" + current_time + "</datetime></metadata>"
    #get xml page if city available + format:
    if city_name not in city_codes:
        print("city name is not available, try again!")
        return
    else:
        url = r"https://api.nextbike.net/maps/nextbike-live.xml?city=" + str(city_codes[city_name])
        r = requests.get(url)
        xml_text = r.text
        #add metadata tag:
        xml_text = xml_text.replace("<markers><country", "<markers>"+tag+"<country")
        xml_text = xml_text.replace("><", ">\n<")
        #write to file in subdirectory:
        path = r"C:\Users\vck\Documents\Python Scripts\bike_project\grabbed_xmls"
        os.chdir(path)
        file_name = filename_part + ".xml"
        file = open(file_name, "w", encoding="utf-8")
        file.write(xml_text)
        file.close()

def my_main(interval, stop_time, city_name):                #!interval = "half-hourly", "hourly" or "daily"//stop_time in format: "DD/MM/YY/hh:mm:ss"//city_name = see above in dictionary!
    get_xml(city_name)
    if interval == "half-hourly":
        schedule.every(30).minutes.do(get_xml, city_name)   #NOT like usual method/param calls! NOT ".do(get_xml(city_name))"!
    elif interval == "hourly":
        schedule.every().hour.do(get_xml, city_name)
    elif interval == "daily":
        #get current time:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        schedule.every().day().at(current_time).do(get_xml, city_name)
    else:
        print("wrong interval, try again")
        return 
    while True:
        schedule.run_pending()
        #time.sleep(10)
        if get_times()[0][:-2] == stop_time[:-2]:
            break

###CALL:
my_main("hourly", "22/02/22/23:30:00", "Köln")


