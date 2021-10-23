import urllib.request
from pprint import pprint
from html_table_parser.parser import HTMLTableParser
from menus import menus
#from datetime import datetime


def url_get_contents(url):
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()


def get_menu(loc, meal_type):
    foods = []
    day_of_the_week = 0
    url = menus[loc][meal_type]
    xhtml = url_get_contents(url).decode('utf-8')

    p = HTMLTableParser()
    p.feed(xhtml)
    tables = p.tables
    counter = 0
    for table in tables[day_of_the_week]:
        if (counter != 0):
            foods.append(table[0])
        counter += 1
    return foods
