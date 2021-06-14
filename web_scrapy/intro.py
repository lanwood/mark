# requests
# BeautifulSoup

# pip install requests
# pip install bs4

import requests
from bs4 import BeautifulSoup
import re

import MySQLdb

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


def get_house_info(house_url):
    soup = get_page(house_url)
    price = soup.find('span', class_='total').text
    house_info = soup.find_all('p')
    area = house_info[0].text[3:]
    location = house_info[6].text[3:]
    info = {
        '价格': price,
        '面积': area,
        '位置': location
    }
    return info


# 连接数据库
DATABASE = {
    'host': '127.0.0.1',
    'database': 'Examination',
    'user': 'root',
    'password': '123456',
    'charset': 'utf8mb4'
}

def get_db(setting):
    return MySQLdb.connect(**setting)

def insert(db, house):
    values = "'{}'," * 2 + "'{}'"
    sql_value = values.format(house['价格'], house['面积'], house['位置'])
    # sql = ("\n"
    #        "        insert into `house` (`price`, `area`, `location`) values ({}, )\n"
    #        "    ").format(sql_value)
    sql = """
        insert into `house`(`price`, `area`, `location`) values ({})
    """.format(sql_value)
    print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

import time
db = get_db('')
links = get_links('')
for link in links:
    time.sleep(2)
    house = get_house_info(link)
    print(house, end='\r')
    insert(db, house)