# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VacanciescollectItem(scrapy.Item):
    # define the fields for your item here like:
    vacancy_name = scrapy.Field()
    vacancy_salary = scrapy.Field()
    min_vacancy_salary = scrapy.Field()
    max_vacancy_salary = scrapy.Field()
    vacancy_link = scrapy.Field()
    curency = scrapy.Field()
    terms = scrapy.Field()
    _id = scrapy.Field()

