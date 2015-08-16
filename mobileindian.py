#!/usr/bin/env python

from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
from mongoengine import *
import logging


LOG_FILENAME = '/var/log/mongodb/webcrawler.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG, )

brands = ["Samsung", "Apple", "Blackberry", "Nokia", "Micromax", "Sony", "Motorola", "LG", "HTC", "Karbonn",
          "Spice Mobiles", "Xolo", "Lava Mobiles", "Lenovo", "Huawei"]


class Page(Document):
    db_brand_name = StringField()
    db_title = StringField()
    db_url = StringField()
    db_page_source = StringField()


base_url = "http://www.themobileindian.com"

connect('mobile_indian')


for brand in brands:
    page = 1
    print(brand)
    while page <= 10:
        try:
            url = "http://www.themobileindian.com/handset-guide/mobile.html?brand=" + str(brand) + "&page=" + str(page)
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text)
            for b in soup.find_all('b'):
                try:
                    for mobile in b.find_all('a'):
                        mobile_url = base_url + mobile.get('href')
                        print mobile_url
                        source_code_mobile = requests.get(mobile_url)
                        plain_text_mobile = source_code_mobile.text
                        mobile_soup = BeautifulSoup(plain_text_mobile)
                        mobile_title = str(mobile.text)
                        logging.info("\n\n*****" + mobile_title + " specs successfully gathered*****")
                        print(mobile_title)
                        Page(db_brand_name=brand, db_title=mobile_title, db_url=mobile_url,
                             db_page_source=plain_text_mobile.encode('utf-8')).save()
                        logging.info("\n*****" + mobile_title + " successfully saved in database*****\n")
                except:
                    logging.error("Basic Error!! One device skipped")
            page += 1
        except:
            page += 1
            logging.error("Some Basic Error!! Few Devices Skipped")
