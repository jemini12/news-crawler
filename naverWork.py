import requests
import datetime
import json
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(hosts="http://news-crawler-es-1426481898.ap-northeast-2.elb.amazonaws.com:9200/")

target_source = "https://m.naver.com/naverapp/?cmd=onMenu&version=3&menuCode=NEWS"
portal = "naver"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
# options.add_argument('window-size=1200x600')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

#chrome드라이버가 PATH 환경변수 설정이 되어있지 않다면 executable_path 옵션으로 chromedriver 위치 지정
driver = webdriver.Chrome(chrome_options=options, executable_path="/usr/local/bin/chromedriver")

driver.implicitly_wait(time_to_wait=20)
driver.get(url=target_source)
boxes = driver.find_elements_by_class_name('ccj_journal_box')

documents = []
for box in boxes:
    article = box.find_element_by_class_name('ut_t')
    title = str(article.get_attribute('innerText'))
    source = target_source
    provider = box.find_element_by_class_name(
        'ccj_btn_subscribe').get_attribute('data-press')
    news_id = box.find_element_by_class_name('ut_a').get_attribute('data-aid')
    documents.append(
        {
            '_index': "naver-news-articles-v1",
            '_source': {
                "portal": portal,
                "title": title,
                "source": target_source,
                "provider": provider,
                "timestamp": str(datetime.datetime.now()),
                "newsID": news_id
            }
        }
    )
    helpers.bulk(es, documents)

print(documents)
driver.close()
