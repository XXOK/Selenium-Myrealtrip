from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import os
import json
import time

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_SECRET_DIR = os.path.join(BASE_DIR, '.config')
CONFIG_SETTINGS_COMMON_FILE = os.path.join(CONFIG_SECRET_DIR, 'account.json')


class SearchTest(unittest.TestCase):

    def __init__(self, x):
        super().__init__()
        self.x = x

    def moveTab(self, x):
        window_before = self.driver.window_handles[x]
        self.driver.switch_to_window(window_before)
        return time.sleep(2)

    def setUp(self):
        self.chromeDriver = PATH('../drivers/chromedriver')
        self.driver = webdriver.Chrome(executable_path=self.chromeDriver)
        self.wait = WebDriverWait(self.driver, 5)

    def runTest(self):

        config_secret = json.loads(open(CONFIG_SETTINGS_COMMON_FILE).read())
        name = config_secret['ACCOUNT']['NAME']
        phone = config_secret['ACCOUNT']['PHONE']
        email = config_secret['ACCOUNT']['EMAIL']
        password = config_secret['ACCOUNT']['PASSWORD']

        main_url = config_secret['ACCOUNT']['URL']
        item_url = main_url + "offers/33751"

        #TODO 1. 메인 화면 접속

        self.driver.get(main_url)

        self.driver.maximize_window()

        #TODO 2. 여행지 검색하기

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gtm-gnb-search '))).click()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'search-input'))).click()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'search-input'))).send_keys('후쿠오카')

        #TODO 3. 여행지

        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'text-lg')))[0].click()
        # 여행지 검색 결과 첫번째

        self.moveTab(1)

        cities_detail_title = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'country__title--kr'))).text

        if not '후쿠오카' == cities_detail_title:
            raise Exception('여행지 상세화면이 검색 내용과 상이합니다.')

        self.driver.close()

        self.moveTab(0)

        #TODO 4. 여행 상품

        item_list_title = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'offer-title')))[0].text
        # 여행 상품 리스트, 첫번째 상품 제목

        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'gtm-search-offer')))[0].click()

        self.moveTab(1)

        item_detail_title = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'offer-title'))).text
        # 여행 상품 상세화면 제목

        if not item_list_title == item_detail_title:
            raise Exception('클릭한 여행 상품의 결과 화면이 상이합니다.')

        self.driver.close()

        self.moveTab(0)

        #TODO 4-1. 여행 상품 > 검색 결과

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'last'))).click()
        # 마지막 페이지로 이동

        forward_end_page = int(self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'page')))[3].text)
        # 마지막 페이지 -1

        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'page')))[4].click()

        items = len(self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'gtm-search-offer'))))
        # 마지막 페이지 검색 결과 개수

        foo = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'number-of-result'))).text

        items_result = int(foo.split('개')[0])

        if not forward_end_page*10+items == items_result:
            raise Exception('검색 결과 개수가 실제 검색 결과 개수와 상이합니다.', forward_end_page*10+items, items_result)


    def tearDown(self):
        self.driver.quit()