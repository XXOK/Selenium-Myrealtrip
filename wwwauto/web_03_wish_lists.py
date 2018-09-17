from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import unittest
import os
import json
import time
import random

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_SECRET_DIR = os.path.join(BASE_DIR, '.config')
CONFIG_SETTINGS_COMMON_FILE = os.path.join(CONFIG_SECRET_DIR, 'account.json')


class WishListsTest(unittest.TestCase):

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

        # TODO 2. 계정 로그인

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gtm-gnb-signin'))).click()

        self.wait.until(EC.visibility_of_element_located((By.NAME, 'user[email]'))).send_keys(email)

        self.wait.until(EC.visibility_of_element_located((By.NAME, 'user[password]'))).send_keys(password)

        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'btn-wrap')))[2].click()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'profile-photo '))).click()

        userName = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.gnb-popup-menu__item--profile > .text'))).text

        if not userName == name:
            raise Exception('로그인 계정 정보가 올바르지 않습니다.')

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'profile-photo '))).click()

        #TODO 3. 위시 리스트 진입

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "profile-photo "))).click()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gtm-gnb-wishlist'))).click()
        # 위시 리스트 버튼 클릭

        #TODO 4. 위시 리스트 유효성 검증

        wish_lists_card = len(self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'wishlists-card'))))
        # 위시 리스트 엘리먼트 개수 (1개라는 가정)
        print(wish_lists_card)

        like_count = int(self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'like-count'))).text)
        # 위시 리스트 엘리먼트 상품 개수 (1개라는 가정)

        sub_title = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'wishlists-header-subtitle'))).text
        # 위시 리스트 개수 카운트 영역

        sub_title_first = sub_title.split('총')

        sub_title_second = sub_title_first[0].split('개')
        # 서브 타이틀 도시 개수

        sub_title_third = sub_title_second[1].split('개')
        # 서브 타이틀 상품 개수

        if not wish_lists_card == sub_title_second:
            if not like_count == sub_title_third:
                raise Exception('카운팅되는 상품 개수가 실제 위시 리스트 상품 개수와 상이합니다.', like_count, sub_title_third)
            raise Exception('카운팅되는 도시 개수가 실제 위시 리스트 도시 개수와 상이합니다.', wish_lists_card, sub_title_second)

    def tearDown(self):
        self.driver.quit()