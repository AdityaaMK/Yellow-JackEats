import urllib.request
from pprint import pprint
from html_table_parser.parser import HTMLTableParser

menus = {
    "north-ave-dining": {
        "breakfast": "https://techdining.nutrislice.com/menu/north-ave-dining-hall/breakfast/carbcounts",
        "lunch": "https://techdining.nutrislice.com/menu/north-ave-dining-hall/lunch/carbcounts",
        "dinner": "https://techdining.nutrislice.com/menu/north-ave-dining-hall/dinner/carbcounts"
    },
    "brittain": {
        "breakfast": "https://techdining.nutrislice.com/menu/brittain/breakfast/carbcounts",
        "lunch": "https://techdining.nutrislice.com/menu/brittain/lunch/carbcounts",
        "dinner": "https://techdining.nutrislice.com/menu/brittain/dinner/carbcounts"
    },
    "west-village": {
        "breakfast": "https://techdining.nutrislice.com/menu/west-village/breakfast/carbcounts",
        "brunch": "https://techdining.nutrislice.com/menu/west-village/brunch/carbcounts",
        "lunch": "https://techdining.nutrislice.com/menu/west-village/lunch/carbcounts",
        "dinner": "https://techdining.nutrislice.com/menu/west-village/dinner/carbcounts"
    }
}


def url_get_contents(url):
    """ Opens a website and read its binary contents (HTTP Response Body) """
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()


def get_menu(day_of_the_week, loc, meal_type):
    url = menus[loc][meal_type]
    xhtml = url_get_contents(url).decode('utf-8')

    p = HTMLTableParser()
    p.feed(xhtml)
    tables = p.tables
    counter = 0
    for table in tables[day_of_the_week]:
        if (counter != 0):
            print(table[0])
        counter += 1

get_menu(2, "west-village", "lunch")