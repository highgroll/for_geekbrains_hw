# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    account_name = scrapy.Field()
    tag = scrapy.Field()
    follower_user_name = scrapy.Field()
    follower_id = scrapy.Field()
    photo = scrapy.Field()
    sub_user_name = scrapy.Field()
    sub_id = scrapy.Field()
    sub_link = scrapy.Field()
    _id = scrapy.Field()