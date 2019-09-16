from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
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


class Test(unittest.TestCase):

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

        # 1. 메인 화면 접속

        self.driver.get(main_url)

        self.driver.set_window_size(1600,1000)

        # 2. 로그인

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "gtm-gnb-signin"))).click()

        self.wait.until(EC.visibility_of_element_located((By.NAME, "user[email]"))).send_keys(email)

        self.wait.until(EC.visibility_of_element_located((By.NAME, "user[password]"))).send_keys(password)

        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "btn-wrap")))[2].click()

        # 3. 오사카 라피트 왕복권 구매

        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".SearchBar-module__input--1Wvjj"))).click()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "SearchFormInput-module__container--2Zmo8"))).click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "SearchBar__input"))).send_keys("오사카")

        time.sleep(1)

        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "SearchFormAutoComplete-module__row--3Cjjm")))[0].click()

        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "LocationCategoryLink-module__link--2utZ6")))[0].click()

        item_list = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "OfferHorizontalCard-module__container--1e3Zk")))

        item_list[0].click()

        datepicker_trigger = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "offer-container__price__select-description")))

        self.driver.execute_script("arguments[0].scrollIntoView()", datepicker_trigger)

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "offer-container__price__datepicker"))).click()

        datepicker_next = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "Calendar_Nav_Button")))

        datepicker_next[1].click()
        time.sleep(2)

        datepicker_date = self.driver.find_elements_by_class_name('CalendarDay__default_2')

        datepicker_date[27].click()
        time.sleep(2)

        el = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "offer-container__price__select")))
        el2 = Select(el[1])
        el2.select_by_visible_text("1명")

        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "app-button")))[0].click()

        time.sleep(2)

    def tearDown(self):
        self.driver.quit()