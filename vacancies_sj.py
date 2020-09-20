import scrapy
from scrapy.http import HtmlResponse
from vacanciesCollect.items import VacanciescollectItem


class VacanciesSjSpider(scrapy.Spider):
    name = 'vacancies_sj'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=Developer']

    def parse(self, response: HtmlResponse):

        vacancies_list = response.xpath("//div[@class='_3mfro PlM3e _2JVkc _3LJqf']//@href").extract()
        for vacancy in vacancies_list:
            yield response.follow(vacancy, callback=self.vacancyParse)

        next_page_button = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']"
                                          "//@href").extract_first()
        if next_page_button:
            yield response.follow(next_page_button, callback=self.parse)

    def vacancyParse(self, response: HtmlResponse):
        vacancy_name = response.xpath('//h1//text()').extract_first()
        vacancy_salary = response.xpath("//span[@class='_1OuF_ ZON4b']//text()").extract()
        vacancy_link = response.url
        yield VacanciescollectItem(vacancy_name=vacancy_name, vacancy_salary=vacancy_salary, vacancy_link=vacancy_link)