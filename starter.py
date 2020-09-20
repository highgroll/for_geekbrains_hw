from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from vacanciesCollect import settings
from vacanciesCollect.spiders.vacancies_hh import HhruSpider
from vacanciesCollect.spiders.vacancies_sj import VacanciesSjSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(VacanciesSjSpider)
    process.start()