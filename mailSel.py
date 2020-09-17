from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
chrome_option = Options()
chrome_option.add_argument('start-maximized')
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
data_base = client['letters']
mail = data_base.mail

driver = webdriver.Chrome(options=chrome_option)
driver.get('https://m.mail.ru/login')

login = driver.find_element_by_name('Login')
login.send_keys('study.ai_172@mail.ru')
time.sleep(0.3)
password = driver.find_element_by_name('Password')
password.send_keys('NextPassword172')
time.sleep(0.3)
password.send_keys(Keys.ENTER)
time.sleep(0.3)

link = driver.find_element_by_class_name('messageline__link')
first_link = link.get_attribute('href')
driver.get(first_link)
letter = {}

while True:
    origin = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME, 'strong'))).text
    name = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'readmsg__theme'))).text
    date = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'readmsg__mail-date'))).text
    content = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'readmsg__body'))).text
    letter['origin'] = origin
    letter['name'] = name
    letter['date'] = date
    letter['content'] = content
    mail.insert_one(letter)

    try:
        next_letter_bottom = WebDriverWait(driver,10).\
            until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,'Следующее')))
        next_letter_bottom.click()
    except exceptions.TimeoutException:
        break
driver.close()
print('Чтение писем завершено. Информация помещена в базу данных.')