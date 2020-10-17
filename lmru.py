import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroyMerlin.items import LeroymerlinItem

class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        self.start_urls = [f'https://spb.leroymerlin.ru/search/?q={search}']
        self.query = search
        super().__init__()

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath("//a[@slot='name']")
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

        next_page = response.xpath("//a[contains(@class, 'next-paginator-button')]")
        for link in next_page:
            yield response.follow(link, callback=self.parse)
            break

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("price", "//span[@slot='price']/text()")
        loader.add_xpath("photo", "//img[@alt='product image']/@src")
        loader.add_xpath("details_keys", "//div[@class='def-list__group']//dd/text()")
        loader.add_xpath("details_items", "//div[@class='def-list__group']//dd/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
