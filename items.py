import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def price_to_float(price):
    if price:
        return float(price.replace(' ', ''))
    return price

def clean_str(value: str):
    if value:
        return value.strip()
    return value

def clean_dot(dot):
    if dot:
        return dot.replace('.', '')
    return dot

class LeroymerlinItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_to_float), output_processor=TakeFirst())
    photo = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    details_keys = scrapy.Field(input_processor=MapCompose(clean_str, clean_dot))
    details_items = scrapy.Field(input_processor=MapCompose(clean_str))
    details = scrapy.Field()
    query = scrapy.Field()
    updated = scrapy.Field()
    _id = scrapy.Field()
