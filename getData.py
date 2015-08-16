#!/usr/bin/env python

import cgi, cgitb
from pymongo import MongoClient
from mongoengine import *

cgitb.enable()

connect('phonearena')

class Page(Document):
    db_brand_name = StringField()
    db_title = StringField()
    db_url = StringField()
    db_page_source = StringField()
print("Content-type:text/html")
print("")
print("<html>")
print("<head>")
print("<title>Results</title>")
print('<meta charset="utf-8">')
print('<meta name="viewport" content="width=device-width, initial-scale=1">')
print('<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">')
print('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>')
print('<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>')
print("</head>")
print("<body>")


print("<table class=\"table table-striped\"><thead><tr><th>Serial#</th><th>Brand</th><th>Device</th><th>Url</th></tr></thead><tbody>")

count = 1

for post in Page.objects[:1000]:
    print("<tr>")
    print("<td>")
    print(count)
    print("</td>")
    print("<td>")
    print(post.db_brand_name[7:-8])
    print("</td>")
    print("<td>")
    print(post.db_title[7:-13].encode('utf-8'))
    print("</td>")
    print("<td>")
    print(post.db_url)
    print("</td>")
    print("</tr>")
    count += 1

print("</tbody>")
print("</table>")
print("</body>")
print("</html>")