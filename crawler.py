#!/usr/bin/env python

import cgi, cgitb
from bs4 import BeautifulSoup
from pymongo import MongoClient
from mongoengine import *
import requests

cgitb.enable()

class Page(Document):
    title = StringField()
    url = StringField()
    page = StringField()
    location = StringField()
    description = StringField()

connect('web_crawler')

visited = []

form = cgi.FieldStorage() 

# Get data from fields
loc = form.getvalue('loc')
job  = form.getvalue('job')

print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Results</title>")
print("</head>")
print("<body>")
print("Hello World" + str(loc) + str(job))

def find(max):
    page = 1
    url = "http://www.indeed.co.in/jobs?q="
    a="Software"
    b="Lucknow"
    #c = input()
    #max = c
    url = url + str(a) + "&l=" + str(b)
    while page <= max:
        source_code = requests.get(url)
        plain_text = source_code.text
        #print(plain_text)
        soup = BeautifulSoup(plain_text)
        #print(soup.prettify)
        try:
            for div in soup.find_all('div', {'class': 'row  result'}):
                if div.find('div',{'class': 'iaP'}):
                    visited.append(div.find('a', {'itemprop': 'title'}))
        except:
            print("error")
        url = "" + url + "&start=" + str(page) + "0"
        page += 1

find(2)
i = 1

print(visited)
for link in visited :
    try:
        newurl="http://www.indeed.co.in" + link.get('href')
    except:
        i-=1
    try:
        print(str(i) + ") " + "<h4>"+ "<a href=" + newurl + " target=\"_blank\">"+ link.get('title') +"</a></h4>")
        source_code = requests.get(newurl)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        url = newurl
        title = soup.find('span', {'class': 'company'}).text
        location = soup.find('span', {'class': 'location'}).text
        description = soup.find('span', {'class': 'summary'}).text
        page = soup
        print("Company: " + soup.find('span', {'class': 'company'}).text + "<br>")
        print("Location: " + soup.find('span', {'class': 'location'}).text + "<br>")
        print("Description:\n             " + soup.find('span', {'class': 'summary'}).text + "<br><br><br>")
        Page(title=title, url=url, location=location, description=description, page=page).save()
    except:
        print("<br>")
    i += 1

print("</body>")
print("</html>")
