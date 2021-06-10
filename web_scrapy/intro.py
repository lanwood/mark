# requests
# BeautifulSoup

# pip install requests
# pip install bs4

import requests
from bs4 import BeautifulSoup
import re

url = "https://fz.lianjia.com/zufang/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

links_div = soup.find_all('div', class_="content__list--item")
links = [div.a.get('href') for div in links_div]
print(links)


def get_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_links(link_url):
    soup = get_page(link_url)
    links_div = soup.find_all('div', class_="content__list--item")
    links = [div.a.get('href') for div in links_div]
    return links


house_url = "https://fz.lianjia.com/apartment/25565.html"
soup = get_page(house_url)
title = soup.find('span', class_="brand-title").text.strip()
# price_list = soup.find_all('span', class_=re.compile("^fr$"))
# price_list = soup.find_all('span', attrs={'class': re.compile(r"^fr$")})
price_list = soup.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ['fr'])
print(len(price_list))
print(price_list)
if len(price_list) > 0:
    print(price_list[0].text.strip())
print(title)
