# Сбор информации с сайта SuperJob 

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re

position = input('Введите интересующую позицию: ')
page = 2
main_link = 'https://www.superjob.ru/vacancy/search/'

while True:
    params = {'keywords': position, 'noGeo': 1, 'page': page}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/85.0.4183.83 Safari/537.36'}

    resp = requests.get(main_link, params=params, headers=headers)
    soup = bs(resp.text, 'html.parser')
    vacancies_list = soup.find_all('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})
    if len(vacancies_list) == 0:
        break

    vacancies = []

    for vacancy in vacancies_list:
        vacancy_info = {}
        vacancy_name = vacancy.find('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'}).getText()
        vacancy_salary = vacancy.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText()
        if vacancy_salary.startswith('от') == True:
            vacancy_salary = [re.sub(r'[^0-9]+', r'', vacancy_salary), 'None', 'руб.']
        elif vacancy_salary.startswith('до') == True:
            vacancy_salary = ['None', re.sub(r'[^0-9]+', r'', vacancy_salary), 'руб.']
        elif len(vacancy_salary) == 0 or vacancy_salary.startswith('По') == True:
            vacancy_salary = ['None', 'None']
        else:
            vacancy_salary = re.sub(r'[^0-9—]+', r'', vacancy_salary)
            vacancy_salary = vacancy_salary.split('—')
            vacancy_salary.append('руб.')
        vacancy_link = 'https://www.superjob.ru' + vacancy.find('a', {'target': '_blank'})['href']
        site = 'superjob.ru'
        vacancy_info['name'] = vacancy_name
        vacancy_info['salary'] = vacancy_salary
        vacancy_info['link'] = vacancy_link
        vacancy_info['site'] = site
        vacancies.append(vacancy_info)
    page += 1
    pprint(vacancies)

