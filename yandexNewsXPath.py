from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
data_base = client['news_DB']
news_yandex = data_base.news_yandex

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/85.0.4183.102 Safari/537.36'}
main_link = 'https://yandex.ru/news/rubric/world'
response = requests.get(main_link, headers=header)

dom = html.fromstring(response.text)
news_items = dom.xpath("//article[contains(@class,'mg-card news-card news-card')]")

for el in news_items:
    news = {}
    source = el.xpath(".//span[@class='mg-card-source__source']/a/text()")
    name = el.xpath(".//h2[@class='news-card__title']/text()")
    link = el.xpath(".//span[@class='mg-card-source__source']/a/@href")
    date = el.xpath(".//span[@class='mg-card-source__time']/text()")
    news['source'] = source
    news['name'] = name
    news['link'] = link
    news['date'] = date
    news_yandex.insert_one(news)
