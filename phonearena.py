#!/usr/bin/env python

from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
from mongoengine import *
import logging


LOG_FILENAME = '/var/log/mongodb/webcrawler.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    )
brands = []


class Page(Document):
    db_brand_name = StringField()
    db_title = StringField()
    db_url = StringField()
    db_page_source = StringField()


base_url = "http://www.phonearena.com"


def find_brands():
    url = "http://www.phonearena.com/phones/manufacturers"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    try:
        for div in soup.find_all('a', {'class': 'ahover'}):
            brand_url = base_url + str(div.get('href'))
            brands.append(brand_url)
    except:
        logging.error("*****Error in Saving Brand Names*****")


connect('phonearena')

find_brands()

for brand in brands:
    url = brand
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    brand_title = str(soup.find('title'))
    print(brand_title)
    page = 1
    while page <= 100:
        try:
            url = brand + "/page/" + str(page)
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text)
            for mobile in soup.find_all('a', {'class': 'atext'}):
                mobile_url = base_url + mobile.get('href')
                source_code_mobile = requests.get(mobile_url)
                plain_text_mobile = source_code_mobile.text
                mobile_soup = BeautifulSoup(plain_text_mobile)
                mobile_title = str(mobile_soup.find('title'))
                logging.info("\n\n*****" + str(mobile_title)[7:-8]+" successfully gathered*****")
                print(mobile_title)
                Page(db_brand_name=str(brand_title), db_title=str(mobile_title), db_url=mobile_url,
                     db_page_source=plain_text_mobile.encode('utf-8')).save()
                logging.info("\n*****"+str(mobile_title)[7:-8]+" successfully saved in database*****\n")
            page += 1
        except:
            page += 1
            logging.error(errors)
