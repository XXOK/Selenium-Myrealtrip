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


class PaymentTest(unittest.TestCase):

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

        self.driver.maximize_window()

        # 2. 로그인

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "gtm-gnb-signin"))).click()

        self.wait.until(EC.visibility_of_element_located((By.NAME, "user[email]"))).send_keys(email)

        self.wait.until(EC.visibility_of_element_located((By.NAME, "user[password]"))).send_keys(password)

        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "btn-wrap")))[2].click()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "profile-photo "))).click()

        userName = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".gnb-popup-menu__item--profile > .text"))).text

        if not userName == name:
            raise Exception("로그인 계정 정보가 올바르지 않습니다.")

        # 3. 오사카 라피트 왕복권 구매

        self.driver.get(item_url)

        calendarBtn = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "offer-title")))

        self.driver.execute_script("arguments[0].scrollIntoView()", calendarBtn)
        time.sleep(2)

        self.wait.until(EC.visibility_of_element_located((By.ID, "calendarBtn"))).click()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, " ui-datepicker-days-cell-over"))).click()

        self.driver.execute_script("arguments[0].scrollIntoView()", calendarBtn)
        time.sleep(1)

        self.wait.until(EC.visibility_of_element_located((By.ID, "optionBtn"))).click()

        self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".input-group-btn > button")))[1].click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "checkPriceBtn"))).click()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "reserve-btn"))).click()

        # 4. 결제 정보 입력

        emailInput = self.wait.until(EC.visibility_of_element_located((By.ID, "input-email")))
        emailInputValue = emailInput.get_attribute("value")

        if not emailInputValue == email:
            raise Exception("구매자 정보의 이메일 주소가 올바르지 않습니다.")

        confirmInput = self.wait.until(EC.visibility_of_element_located((By.ID, "input-email-confirm")))
        confirmInputValue = confirmInput.get_attribute("value")

        if not confirmInputValue == email:
            raise Exception("구매자 정보의 이메일 주소(확인)가 올바르지 않습니다.")

        phoneInput = self.wait.until(EC.visibility_of_element_located((By.NAME, "reservation[phone_number]")))
        phoneInputValue = phoneInput.get_attribute("value")

        if not phoneInputValue == phone:
            raise Exception("구매자 정보의 휴대폰 번호가 올바르지 않습니다.")

        ageBoundary = self.wait.until(EC.visibility_of_element_located((By.NAME, "user_privacy[age]")))
        ageBoundary.find_elements_by_tag_name("option")[2].click()

        reservationPurpose = self.wait.until(EC.visibility_of_element_located((By.NAME, "reservation[purpose]")))
        reservationPurpose.find_elements_by_tag_name("option")[1].click()

        self.wait.until(EC.visibility_of_element_located((By.NAME, "reservation[message]"))).send_keys("자동화 테스트입니다.")

        paymentTitle = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "title")))[3]

        self.driver.execute_script("arguments[0].scrollIntoView()", paymentTitle)
        time.sleep(2)

        self.driver.find_element_by_id("type-vbank").click()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "checkbox-custom"))).click()

        # self.wait.until(EC.visibility_of_element_located((By.ID, "reservation-btn"))).click()


    def tearDown(self):
        self.driver.quit()