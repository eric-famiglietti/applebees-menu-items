from bs4 import BeautifulSoup, SoupStrainer
import json
import requests


URL = 'https://www.applebees.com/en/menu'
OUTPUT = 'menu_items.json'


page = requests.get(URL)
strainer = SoupStrainer('script', type='text/javascript')
soup = BeautifulSoup(page.content, 'html.parser', parse_only=strainer)

# Sanitize and parse JSON data stored in script tag.
data = soup.find_all('script')[3].string[58:-63]
data = json.loads(data)

menu_items = []
for category in data['data']['Categories']:
    for menu_item in category['MenuItems']:
        menu_items.append({
            'category': category['Name'],
            'description': menu_item['Description'] or None,
            'image': menu_item['ImageLarge'],
            'name': menu_item['Name'],
        })

with open(OUTPUT, 'w') as f:
    f.write(json.dumps(menu_items))
