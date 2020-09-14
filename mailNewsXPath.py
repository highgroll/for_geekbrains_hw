from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
data_base = client['news_DB']
news_mail = data_base.news_mail

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/85.0.4183.102 Safari/537.36'}
main_link = 'https://news.mail.ru/politics/'
response = requests.get(main_link, headers=header)

dom = html.fromstring(response.text)
news_items = dom.xpath("////div[contains(@class,'newsitem_height_fixed js-ago-wrapper js-pgng_item')]")

for el in news_items:
    news = {}
    source = el.xpath(".//span[@class='newsitem__param']/text()")
    name = el.xpath(".//span[@class='newsitem__title-inner']/text()")
    link = el.xpath(".//a[@class='newsitem__title link-holder']//@href")
    date = el.xpath(".//span[@class='newsitem__param js-ago']/text()")
    news['source'] = source
    news['name'] = name
    news['link'] = link
    news['date'] = date
    news_mail.insert_one(news)
