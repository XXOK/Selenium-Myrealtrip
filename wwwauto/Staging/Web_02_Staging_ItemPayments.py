from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from time import sleep
import unittest
import os
import json
import time
import pdb

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

CONFIG_SETTINGS_COMMON_FILE = PATH('/Users/yeonshin/Selenium-Myrealtrip/.config/staging_account.json')

class Test(unittest.TestCase):

    def __init__(self, x):
        super().__init__()
        self.x = x

    def moveTab(self, x):
        window_before = self.driver.window_handles[x]
        self.driver.switch_to_window(window_before)
        return time.sleep(2)

    def setUp(self):
        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # options.add_argument('window-size=1600x1080')
        # options.add_argument("disable-gpu")
        self.chromeDriver = PATH('/Users/yeonshin/Selenium-Myrealtrip/drivers/chromedriver')
        self.driver = webdriver.Chrome(executable_path=self.chromeDriver)
        self.wait = WebDriverWait(self.driver, 10)

    def runTest(self):

        wd = self.driver
        wait = WebDriverWait(wd, 10)

        config_secret = json.loads(open(CONFIG_SETTINGS_COMMON_FILE).read())
        name = config_secret['ACCOUNT']['NAME']
        phone = config_secret['ACCOUNT']['PHONE']
        wording = config_secret['ACCOUNT']['WORDING']
        code = config_secret['ACCOUNT']['CODE']
        normal_email = config_secret['ACCOUNT']['NORMAL_EMAIL']
        normal_password = config_secret['ACCOUNT']['NORMAL_PASSWORD']
        facebook_email = config_secret['ACCOUNT']['FACEBOOK_EMAIL']
        facebook_password = config_secret['ACCOUNT']['FACEBOOK_PASSWORD']
        naver_email = config_secret['ACCOUNT']['NAVER_EMAIL']
        naver_password = config_secret['ACCOUNT']['NAVER_PASSWORD']
        login_email = config_secret['ACCOUNT']['LOGIN_EMAIL']
        login_password = config_secret['ACCOUNT']['LOGIN_PASSWORD']

        main_url = config_secret['ACCOUNT']['STAGING_URL']
        item_url = main_url + "/offers/24477"

        self.driver.set_window_size(1600,1080)
        self.driver.get(item_url)

        # TODO - 이메일 계정 로그인

        # 로그인 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "GlobalNavItems__item")))[1].click()

        # 이메일 계정 입력
        wait.until(EC.visibility_of_element_located((By.NAME, 'user[email]'))).send_keys(login_email)

        # 비밀번호 입력
        wait.until(EC.visibility_of_element_located((By.NAME, 'user[password]'))).send_keys(login_password)

        # 이메일로 로그인 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'btn-wrap')))[2].click()

        # TODO - 금액 조회하기

        # 상품 이미지 영역 변수 할당
        target = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'offer-container__photo--cover')))[1]

        # 상품 이미지 영역 엘리먼트 위치로 스크롤
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        # 날짜 선택 영역 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'offer-container__price__datepicker'))).click()

        # 다음 달 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'Calendar_Nav_Button')))[1].click()

        sleep(2)

        # 한달 뒤 날짜 클릭
        self.driver.find_elements_by_class_name('CalendarDay__default_2')[27].click()

        sleep(2)

        # 옵션 선택 영역 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'offer-container__option'))).click()

        # 옵션 + 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'option-clicked'))).click()

        # 금액 조회화기 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gtm-offer-check-price'))).click()

        # 구매하기 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'offer-container__price__total-result--link'))).click()

        # TODO - 주문서 페이지 주문자 정보 입력

        try:
            # 예약정보 불러오기 팝업 닫기 버튼 클릭
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'Dialog-module__close--3QJG1'))).click()

        except:
            pass

        # 연령대 선택 영역 변수 할당
        target = wait.until(EC.visibility_of_element_located((By.NAME, 'user_privacy[age]')))

        # 연령대 선택 영역 엘리먼트 위치로 스크롤
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        # 여행 목적 option 값 Select 인자로 할당 후 변수 할당
        select = Select(wait.until(EC.visibility_of_element_located((By.NAME, 'reservation[purpose]'))))

        # 여행 목적 혼자 떠나는 여행 선택
        select.select_by_value('alone')

        sleep(1)

        # 상품 가격 변수 할당
        item_price = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'price-container'))).text

        # 포인트 입력 영역에 item_price 입력
        wait.until(EC.visibility_of_element_located((By.NAME, 'promotion[point]'))).send_keys(item_price)

        # 여행자 약관 버튼 클릭
        self.driver.find_element_by_id("checkbox_terms_traveler").click()

        sleep(1)

        # 결제하기 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn--type-primary'))).click()

        # 예약 완료 시 상품 추천 팝업 닫기 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'Dialog-module__close--3QJG1'))).click()

        # '이 상품을 본 여행자가 함께 본 상품' 영역 변수 할당
        target = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'other-title')))

        # '이 상품을 본 여행자가 함께 본 상품' 영역 엘리먼트 위치로 스크롤
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        # 예약내역 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-blue'))).click()

        # TODO - 예약 건 취소하기

        # 취소하기 버튼 변수 할당
        target = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'reservation-cancel-btn')))

        # 취소하기 영역 엘리먼트 위치로 스크롤
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        # 취소하기 버튼 클릭
        target.click()

        # 취소하기 팝업의 예약 취소하기 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'Button-module__large--SJ0aY'))).click()

        # 예약이 취소되었습니다. 얼럿 확인
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'status-cancel')))

        # # TODO - 무통장 결제 (현재 falsh 실행 불가능으로 주석 처리)
        #
        # # 결제정보 무통장 입금 버튼 선택
        # self.driver.find_element_by_id("type-vbank").click()
        #
        # sleep(1)
        #
        # # 전체동의 클릭
        # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'all_p'))).click()
        #
        # # 입금은행 option 값 Select 인자로 할당 후 변수 할당
        # select = Select(wait.until(EC.visibility_of_element_located((By.NAME, 'vactBankCode'))))
        #
        # # 입금은행 우리은행 선택
        # select.select_by_value('20')
        #
        # # 다음 버튼 클릭
        # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn_right'))).click()
        #
        # # 예약 완료 시 상품 추천 팝업 닫기 버튼 클릭
        # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'Dialog-module__close--3QJG1'))).click()
        #
        # # '이 상품을 본 여행자가 함께 본 상품' 영역 변수 할당
        # target = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'other-title')))
        #
        # # '이 상품을 본 여행자가 함께 본 상품' 영역 엘리먼트 위치로 스크롤
        # self.driver.execute_script('arguments[0].scrollIntoView(true);', target)
        #
        # # 예약내역 버튼 클릭
        # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-blue'))).click()

    def tearDown(self):
        self.driver.quit()