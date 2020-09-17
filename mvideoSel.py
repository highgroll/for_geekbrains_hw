from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
chrome_option = Options()
chrome_option.add_argument('start-maximized')
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
data_base = client['goods']
mvideo_goods = data_base.mvideo_goods

driver = webdriver.Chrome(options=chrome_option)
driver.get('https://www.mvideo.ru/')
assert 'М.Видео' in driver.title

while True:
    try:
        next_bottom_block = driver.find_element_by_xpath('//div[contains(text(),"Хиты продаж")]/'
                                                       'ancestor::div[@data-init="gtm-push-products"]')
        next_bottom = WebDriverWait(next_bottom_block, 15).\
                until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="next-btn sel-hits-button-next"]')))
        next_bottom.click()
    except:
        break

goods_items = driver.find_elements_by_css_selector("a.sel-product-tile-title")
for item in goods_items:
    good_info = item.get_attribute('data-product-info')
    mvideo_goods.insert_one(good_info)

driver.close()
print('Сбор информации завершён. Данные помещены в базу.')



