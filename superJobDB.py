from bs4 import BeautifulSoup as bs
import requests
import re
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
data_base = client['vacancies_DB']
vacancies_sj = data_base.vacancies_sj

position = input('Введите интересующую позицию: ')
page = 1
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

    for vacancy in vacancies_list:
        vacancy_info = {}
        vacancy_name = vacancy.find('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'}).getText()
        vacancy_salary_str = vacancy.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText()
        if vacancy_salary_str.startswith('от') == True:
            if vacancy_salary_str.endswith('час') == True:
                vacancy_salary = [int(re.sub(r'[^0-9]+', r'', vacancy_salary_str)), 'None', 'руб.', 'час']
            elif vacancy_salary_str.endswith('день') == True:
                vacancy_salary = [int(re.sub(r'[^0-9]+', r'', vacancy_salary_str)), 'None', 'руб.', 'день']
            else:
                vacancy_salary = [int(re.sub(r'[^0-9]+', r'', vacancy_salary_str)), 'None', 'руб.', 'месяц']
        elif vacancy_salary_str.startswith('до') == True:
            if vacancy_salary_str.endswith('час') == True:
                vacancy_salary = ['None', int(re.sub(r'[^0-9]+', r'', vacancy_salary_str)), 'руб.', 'час']
            elif vacancy_salary_str.endswith('день') == True:
                vacancy_salary = ['None', int(re.sub(r'[^0-9]+', r'', vacancy_salary_str)), 'руб.', 'день']
            else:
                vacancy_salary = ['None', int(re.sub(r'[^0-9]+', r'', vacancy_salary_str)), 'руб.', 'месяц']
        elif len(vacancy_salary_str) == 0 or vacancy_salary_str.startswith('По') == True:
            vacancy_salary = ['None', 'None', 'None', 'None']
        else:
            vacancy_salary_pre = re.sub(r'[^0-9—]+', r'', vacancy_salary_str)
            vacancy_salary_pre = vacancy_salary_pre.split('—')
            vacancy_salary = []
            for el in vacancy_salary_pre:
                el_int = int(el)
                vacancy_salary.append(el_int)
            vacancy_salary.append('руб.')
            if vacancy_salary_str.endswith('час') == True:
                vacancy_salary.append('час')
            elif vacancy_salary_str.endswith('день') == True:
                vacancy_salary.append('день')
            else:
                vacancy_salary.append('месяц')
        vacancy_link = 'https://www.superjob.ru' + vacancy.find('a', {'target': '_blank'})['href']
        site = 'superjob.ru'
        vacancy_info['name'] = vacancy_name
        vacancy_info['salary'] = vacancy_salary
        vacancy_info['link'] = vacancy_link
        vacancy_info['site'] = site

        duplicates = vacancies_sj.find_one({'link': vacancy_link})
        if duplicates == None:
            vacancies_sj.insert_one(vacancy_info)
        else:
            pass
    page += 1