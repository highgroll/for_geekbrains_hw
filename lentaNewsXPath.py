from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
data_base = client['news_DB']
news_lenta = data_base.news_lenta

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/85.0.4183.102 Safari/537.36'}
main_link = 'https://lenta.ru/rubrics/world/'
response = requests.get(main_link, headers=header)

dom = html.fromstring(response.text)
news_items = dom.xpath("//section[@class='b-longgrid-column']/div[contains(@class, 'item')]")

for el in news_items:
    news = {}
    site = 'lenta.ru'
    name = el.xpath(".//a/span/text()")
    for item in name:
        name = item.replace('\xa0', ' ')
    link = el.xpath(".//div[@class='titles']//@href")
    for item in link:
        link = main_link + item
    date = el.xpath(".//span[@class='g-date item__date']/text()")
    news['site'] = site
    news['name'] = name
    news['link'] = link
    news['date'] = date
    news_lenta.insert_one(news)


