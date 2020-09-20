import scrapy
from scrapy.http import HtmlResponse
from vacanciesCollect.items import VacanciescollectItem

class HhruSpider(scrapy.Spider):
    name = 'vacancies_hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://krasnodar.hh.ru/'
                  'search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=big+data']

    def parse(self, response:HtmlResponse):

        vacancies_list = response.css("div.vacancy-serp-item__row_header a.bloko-link::attr(href)").extract()
        for vacancy in vacancies_list:
            yield response.follow(vacancy, callback=self.vacancyParse)

        next_page_button = response.css(
            "a.HH-Pager-Controls-Next::attr(href)").extract_first()
        if next_page_button:
            yield response.follow(next_page_button, callback=self.parse)

    def vacancyParse(self, response:HtmlResponse):
        vacancy_name = response.xpath('//h1//text()').extract_first()
        vacancy_salary = response.xpath("//p[@class='vacancy-salary']//text()").extract()
        vacancy_link = response.url
        yield VacanciescollectItem(vacancy_name=vacancy_name, vacancy_salary=vacancy_salary, vacancy_link=vacancy_link)