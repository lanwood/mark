from bs4 import BeautifulSoup
import urllib.request
import os

prefix = "https://archive.org"
html_doc = "https://archive.org/details/gaodengshuxue0/page/n11"
req = urllib.request.Request(html_doc)
web_page = urllib.request.urlopen(req)
html = web_page.read()

soup = BeautifulSoup(html, 'html.parser')

for k in soup.find_all('a', class_='stealth download-pill'):
    try:
        # make directory
        if not os.path.exists('./auto_download'):
            os.makedirs('auto_download')

        # download links
        link = prefix + k['href']
        book_name = '_'.join(k.get_text().split( )[1:-1])
        if book_name.endswith(".pdf"):
            print("下载图书:" + book_name)
            print(link)
            urllib.request.urlretrieve(link, os.path.join('./auto_download', book_name))
            print("========================================")
    except:
        continue
