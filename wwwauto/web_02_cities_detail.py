from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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


class CitiesDetailTest(unittest.TestCase):

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

        #TODO 2. 인기 여행지 선택

        popular_city_section = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'mrt-popular-city')))

        popular_city_hover = ActionChains(self.driver).move_to_element(popular_city_section)
        # 인기 여행지 마우스 오버
        popular_city_hover.perform()
        time.sleep(1)

        rnd_index = random.choice(range(14))
        print(rnd_index)

        cities_rnd_choice = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'popular-city__item--name')))[rnd_index].text
        # 랜덤으로 선택한 인기 여행지 이름

        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'popular-city__item--name')))[rnd_index].click()
        # 랜덤으로 선택한 인기 여행지 클릭

        cities_detail_title = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'country__title--kr'))).text
        # 랜덤으로 선택한 인기 여행지 상세화면 제목

        if not cities_rnd_choice == cities_detail_title:
            raise Exception('선택한 인기 여행지와 노출되는 상세화면 여행지가 상이합니다.', cities_rnd_choice, cities_detail_title)

        # TODO 3. 여행일정 등록

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'calendar-container__input'))).click()
        # 여행일정 등록 버튼 클릭

        calendar_2nights_3days = int(self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ui-datepicker-today'))).text)+3
        # 여행일정 당일+3

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ui-datepicker-today'))).click()
        # 여행일정 당일 선택

        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//td[@data-handler='selectDay']/a[text()="+"'"+str(calendar_2nights_3days)+"'"+"]"))).click()
        # 여행일정 당일+3 선택

        time.sleep(10)


    def tearDown(self):
        self.driver.quit()