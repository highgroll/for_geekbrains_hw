# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class VacanciescollectPipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.data_base = client.vacancies_DB

    def process_item(self, item, spider):

        list = item['vacancy_salary']

        if spider.name == 'hh.ru':
            if list[0] == 'от ' and list[2] == ' до ':
                min_vacancy_salary = int(re.sub(r'[^0-9]+', r'', list[1]))
                max_vacancy_salary = int(re.sub(r'[^0-9]+', r'', list[3]))
                curency = list[5]
                terms = list[6]
            elif list[0] == 'от ':
                min_vacancy_salary = int(re.sub(r'[^0-9]+', r'', list[1]))
                max_vacancy_salary = 'не указана'
                curency = list[3]
                terms = list[4]
            elif list[0] == 'до ':
                min_vacancy_salary = 'не указана'
                max_vacancy_salary = int(re.sub(r'[^0-9]+', r'', list[1]))
                curency = list[3]
                terms = list[4]
            elif list[0] == 'з/п не указана':
                min_vacancy_salary = 'не указана'
                max_vacancy_salary = 'не указана'
                curency = 'не указана'
                terms = 'не указаны'
            result = {
                'vacancy_name': item['vacancy_name'],
                'min_vacancy_salary': min_vacancy_salary,
                'max_vacancy_salary': max_vacancy_salary,
                'curency': curency, 'terms': terms
            }
        elif spider.name == 'superjob.ru':
            if list[0] == 'По договорённости':
                min_vacancy_salary = 'по договорённости'
                max_vacancy_salary = 'по договорённости'
                curency = 'не указана'
                terms = 'не указаны'
            elif list[0] == 'от':
                min_vacancy_salary = int(re.sub(r'[^0-9]+', r'', list[2]))
                max_vacancy_salary = 'не указана'
                curency = 'руб.'
                terms = list[4]
            elif list[0] == 'до':
                min_vacancy_salary = 'не указана'
                max_vacancy_salary = int(re.sub(r'[^0-9]+', r'', list[2]))
                curency = 'руб.'
                terms = list[4]
            else:
                min_vacancy_salary = int(re.sub(r'[^0-9]+', r'', list[0]))
                max_vacancy_salary = int(re.sub(r'[^0-9]+', r'', list[4]))
                curency = list[6]
                terms = list[8]
            result = {
                'vacancy_name': item['vacancy_name'],
                'min_vacancy_salary': min_vacancy_salary,
                'max_vacancy_salary': max_vacancy_salary,
                'curency': curency, 'terms': terms
            }
        
        collection = self.data_base[spider.name]
        collection.insert_one(result)
        return item
