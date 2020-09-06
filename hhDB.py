from bs4 import BeautifulSoup as bs
import requests
import re
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
data_base = client['vacancies_DB']
vacancies_hh = data_base.vacancies_hh


position = input('Введите интересующую позицию: ')
page = 0
main_link = 'https://hh.ru/search/vacancy'

while True:

    params = {'text': position, 'page': page}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/85.0.4183.83 Safari/537.36'}

    resp = requests.get(main_link, params=params, headers=headers)
    soup = bs(resp.text, 'html.parser')
    vacancies_list = soup.find_all('div', {'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_premium'})
    if len(vacancies_list) == 0:
        break

    for vacancy in vacancies_list:
        vacancy_info = {}
        vacancy_name = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'}).text
        vacancy_salary_str = vacancy.find('div', {'class', 'vacancy-serp-item__sidebar'}).getText()

        if vacancy_salary_str.startswith('от') == True:
            if vacancy_salary_str.endswith('USD') == True:
                vacancy_salary = [int(re.sub(r'[^0-9]+', r'', vacancy_salary_str)), 'None', 'USD']
            else:
                vacancy_salary = [int(re.sub(r'[^0-9]+', r'', vacancy_salary_str)), 'None', 'руб.']
        elif vacancy_salary_str.startswith('до') == True:
            if vacancy_salary_str.endswith('USD') == True:
                vacancy_salary = ['None', int(re.sub(r'[^0-9]+', r'', vacancy_salary_str)), 'USD']
            else:
                vacancy_salary = ['None', int(re.sub(r'[^0-9]+', r'', vacancy_salary_str)), 'руб.']
        elif len(vacancy_salary_str) == 0:
            vacancy_salary = ['None', 'None', 'None']
        else:
            if vacancy_salary_str.endswith('USD') == True:
                vacancy_salary_pre = re.sub(r'[^0-9-]+', r'', vacancy_salary_str)
                vacancy_salary_pre = vacancy_salary_pre.split('-')
                vacancy_salary = []
                for el in vacancy_salary_pre:
                    el_int = int(el)
                    vacancy_salary.append(el_int)
                vacancy_salary.append('USD')
            else:
                vacancy_salary_pre = re.sub(r'[^0-9-]+', r'', vacancy_salary_str)
                vacancy_salary_pre = vacancy_salary_pre.split('-')
                vacancy_salary = []
                for el in vacancy_salary_pre:
                    el_int = int(el)
                    vacancy_salary.append(el_int)
                vacancy_salary.append('руб.')
        vacancy_link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
        site = 'hh.ru'
        vacancy_info['name'] = vacancy_name
        vacancy_info['salary'] = vacancy_salary
        vacancy_info['link'] = vacancy_link
        vacancy_info['site'] = site

        duplicates = vacancies_hh.find_one({'link': vacancy_link})
        if duplicates == None:
            vacancies_hh.insert_one(vacancy_info)
        else:
            pass
    page += 1
