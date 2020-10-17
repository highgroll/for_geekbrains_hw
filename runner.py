from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroyMerlin import settings
from leroyMerlin.spiders.lmru import LmruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    #search = input('Введите параметр поиска: ')
    process.crawl(LmruSpider, search='peach')
    process.start()