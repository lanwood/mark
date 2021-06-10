# requests
# BeautifulSoup

# pip install requests
# pip install bs4

import requests
from bs4 import BeautifulSoup

url = "https://fz.lianjia.com/zufang/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

links_div = soup.find_all('div', class_="pic-panel")
links = [div.a.get('href') for div in links_div]