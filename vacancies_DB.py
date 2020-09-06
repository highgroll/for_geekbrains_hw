from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
data_base = client['vacancies_DB']
vacancies_hh = data_base.vacancies_hh
vacancies_sj = data_base.vacancies_sj

search_param = int(input('Введите размер заработной платы: '))

for element in vacancies_hh.find({'salary': {'$gt': search_param}},{"_id": 0, "site": 0}):
    pprint(element)

for element in vacancies_sj.find({'salary': {'$gt': search_param}},{"_id": 0, "site": 0}):
    pprint(element)



