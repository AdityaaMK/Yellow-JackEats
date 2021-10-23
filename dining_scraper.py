import requests
from bs4 import BeautifulSoup


menus = {
    "north-ave-dining": {
        "breakfast": "https://techdining.nutrislice.com/menu/north-ave-dining-hall/breakfast/",
        "lunch": "https://techdining.nutrislice.com/menu/north-ave-dining-hall/lunch/",
        "dinner": "https://techdining.nutrislice.com/menu/north-ave-dining-hall/dinner"
    },
    "brittain": {
        "breakfast": "https://techdining.nutrislice.com/menu/brittain/breakfast/",
        "lunch": "https://techdining.nutrislice.com/menu/brittain/lunch",
        "dinner": "https://techdining.nutrislice.com/menu/brittain/dinner"
    },
    "west-village": {
        "breakfast": "https://techdining.nutrislice.com/menu/west-village/breakfast",
        "brunch": "https://techdining.nutrislice.com/menu/west-village/brunch",
        "lunch": "https://techdining.nutrislice.com/menu/west-village/lunch",
        "dinner": "https://techdining.nutrislice.com/menu/west-village/lunch"
    }
}

import urllib.request
from html_table_parser import HTMLTableParser

target = 'http://www.twitter.com'

# get website content
req = urllib.request.Request(url=target)
f = urllib.request.urlopen(req)
xhtml = f.read().decode('utf-8')

# instantiate the parser and feed it
p = HTMLTableParser()
p.feed(xhtml)
print(p.tables)