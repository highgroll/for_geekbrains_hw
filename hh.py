# Сбор информации с сайта HeadHanter 

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re

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

    vacancies = []
    for vacancy in vacancies_list:
        vacancy_info = {}
        vacancy_name = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'}).text
        vacancy_salary = vacancy.find('div', {'class', 'vacancy-serp-item__sidebar'}).getText()

        if vacancy_salary.startswith('от') == True:
            if vacancy_salary.endswith('USD') == True:
                vacancy_salary = [re.sub(r'[^0-9]+', r'', vacancy_salary), 'None', 'USD']
            else:
                vacancy_salary = [re.sub(r'[^0-9]+', r'', vacancy_salary), 'None', 'руб.']
        elif vacancy_salary.startswith('до') == True:
            if vacancy_salary.endswith('USD') == True:
                vacancy_salary = ['None', re.sub(r'[^0-9]+', r'', vacancy_salary), 'USD']
            else:
                vacancy_salary = ['None', re.sub(r'[^0-9]+', r'', vacancy_salary), 'руб.']
        elif len(vacancy_salary) == 0:
            vacancy_salary = ['None', 'None']
        else:
            if vacancy_salary.endswith('USD') == True:
                vacancy_salary = re.sub(r'[^0-9-]+', r'', vacancy_salary)
                vacancy_salary = vacancy_salary.split('-')
                vacancy_salary.append('USD')
            else:
                vacancy_salary = re.sub(r'[^0-9-]+', r'', vacancy_salary)
                vacancy_salary = vacancy_salary.split('-')
                vacancy_salary.append('руб.')
        vacancy_link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
        site = 'hh.ru'
        vacancy_info['name'] = vacancy_name
        vacancy_info['salary'] = vacancy_salary
        vacancy_info['link'] = vacancy_link
        vacancy_info['site'] = site
        vacancies.append(vacancy_info)
    page += 1
    pprint(vacancies)
