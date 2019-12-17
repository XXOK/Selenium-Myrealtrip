from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
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

class RegisterAccounts(unittest.TestCase):

    def __init__(self, x):
        super().__init__()
        self.x = x

    def moveTab(self, x):
        window_before = self.driver.window_handles[x]
        self.driver.switch_to_window(window_before)
        return time.sleep(2)

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1600x1080')
        options.add_argument("disable-gpu")
        self.chromeDriver = PATH('/Users/yeonshin/Selenium-Myrealtrip/drivers/chromedriver')
        self.driver = webdriver.Chrome(executable_path=self.chromeDriver)
        # self.driver = webdriver.Chrome(executable_path=self.chromeDriver, options=options)
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
        item_url = main_url + "offers/33751"

        # TODO - 마이리얼트립 메인화면

        self.driver.get(main_url)

        self.driver.set_window_size(1600,1080)

        # TODO - 이메일 계정 회원가입

        # 회원가입 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'GlobalNavItems__item')))[2].click()

        # 이름 입력
        wait.until(EC.visibility_of_element_located((By.NAME, 'user[username]'))).send_keys(name)

        # 이메일 계정 입력
        wait.until(EC.visibility_of_element_located((By.NAME, 'user[email]'))).send_keys(normal_email)

        # 비밀번호 입력
        wait.until(EC.visibility_of_element_located((By.NAME, 'user[password]'))).send_keys(normal_password)

        # 비밀번호 확인 입력
        wait.until(EC.visibility_of_element_located((By.NAME, 'user[password_confirmation]'))).send_keys(normal_password)

        # 비밀번호 확인 변수 할당
        target = wait.until(EC.visibility_of_element_located((By.ID, 'userPasswordConfirm')))

        # 비밀번호 확인 엘리먼트 위치로 스크롤
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        sleep(1)

        # 약관 전체 동의 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.ID, 'agreeAll'))).click()

        # 회원가입 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'Button-module__button--227wS')))[2].click()

        # 휴대폰 번호 입력
        wait.until(EC.visibility_of_element_located((By.NAME, 'user[phone_number]'))).send_keys(phone)

        sleep(1)

        # 문자로 인증번호 보내기 버튼 클릭
        self.driver.find_elements_by_class_name('btn-wrap')[0].click()

        sleep(1)

        # 인증코드 변수 할당
        target= wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'sub-title')))[2]

        # 인증코드 엘리먼트 위치로 스크롤
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        sleep(1)

        # 인증코드 입력
        wait.until(EC.visibility_of_element_located((By.NAME, 'user[verify_code]'))).send_keys(code)

        sleep(2)

        self.driver.find_elements_by_class_name('btn-wrap')[1].click()

        sleep(2)

        self.driver.refresh()

        # TODO - 이메일 계정 로그아웃

        # 프로필 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ProfileNavItems'))).click()

        # 로그아웃 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gtm-gnb-signout'))).click()

        # TODO - 이메일 계정 로그인

        # 로그인 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'GlobalNavItems__item')))[1].click()

        # 이메일 계정 입력
        wait.until(EC.visibility_of_element_located((By.NAME, 'user[email]'))).send_keys(normal_email)

        # 비밀번호 입력
        wait.until(EC.visibility_of_element_located((By.NAME, 'user[password]'))).send_keys(normal_password)

        # 이메일로 로그인 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'btn-wrap')))[2].click()

        # TODO - 이메일 계정 삭제

        # 프로필 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ProfileNavItems'))).click()

        # 프로필 관리 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gtm-gnb-account'))).click()

        # 계정 삭제하기 변수 할당
        target = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'text-sm')))

        # 계정 삭제하기 엘리먼트 위치로 스크롤
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        sleep(1)

        # 계정 삭제하기 버튼 클릭
        target.click()

        sleep(1)

        # 여행을 자주 떠나지 않아서요. 라디오 버튼 클릭
        self.driver.find_element_by_id('reason_0').click()

        # 팝업의 계정 삭제하기 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-submit'))).click()

        # TODO - 페이스북 계정 회원가입

        # 회원가입 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'GlobalNavItems__item')))[2].click()

        # 페이스북으로 회원가입 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'btn-wrap')))[0].click()

        # 이메일 입력
        wait.until(EC.visibility_of_element_located((By.ID, 'email'))).send_keys(facebook_email)

        # 비밀번호 입력
        wait.until(EC.visibility_of_element_located((By.ID, 'pass'))).send_keys(facebook_password)

        # 로그인 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.ID, 'loginbutton'))).click()

        # 약관동의 변수 할당
        target = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'content-title-box')))[2]

        # 약관동의 엘리먼트 위치로 스크롤
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        # 약관 전체 동의 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'checkbox-signup-all'))).click()

        # 회원가입 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-wrap'))).click()

        # TODO - 페이스북 계정 로그아웃

        # 프로필 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ProfileNavItems'))).click()

        # 로그아웃 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gtm-gnb-signout'))).click()

        # TODO - 페이스북 계정 로그인

        # 로그인 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "GlobalNavItems__item")))[1].click()

        # 페이스북으로 로그인 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "btn-sns")))[0].click()

        # TODO - 페이스북 계정 삭제

        # 프로필 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ProfileNavItems'))).click()

        # 프로필 관리 버튼 클
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gtm-gnb-account'))).click()

        # 계정 삭제하기 변수 할당
        target = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'text-sm')))

        # 계정 삭제하기 엘리먼트 위치로 스크롤
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        sleep(1)

        # 계정 삭제하기 버튼 클릭
        target.click()

        sleep(1)

        # 여행을 자주 떠나지 않아서요. 라디오 버튼 클릭
        self.driver.find_element_by_id('reason_0').click()

        # 팝업의 계정 삭제하기 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-submit'))).click()

        # TODO - 네이버 계정 회원가입

        # 회원가입 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'GlobalNavItems__item')))[2].click()

        # 페이스북으로 회원가입 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'btn-wrap')))[1].click()

        sleep(2)

        # 아이디 입력
        self.driver.execute_script("document.getElementsByName('id')[0].value=\'" + naver_email + "\'")

        sleep(1)

        # 비밀번호 입력
        self.driver.execute_script("document.getElementsByName('pw')[0].value=\'" + naver_password + "\'")

        sleep(1)

        # 로그인 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn_global"))).click()

        # 이름 입력
        wait.until(EC.visibility_of_element_located((By.NAME, 'user[username]'))).send_keys(name)

        # 약관동의 변수 할당
        target = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'content-title-box')))[2]

        # 약관동의 엘리먼트 위치로 스크롤
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        # 약관 전체 동의 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'checkbox-signup-all'))).click()

        # 회원가입 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-wrap'))).click()

        # TODO - 네이버 계정 로그아웃

        # 프로필 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ProfileNavItems'))).click()

        # 로그아웃 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gtm-gnb-signout'))).click()

        # TODO - 네이버 계정 로그인

        # 로그인 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "GlobalNavItems__item")))[1].click()

        # 페이스북으로 로그인 버튼 클릭
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "btn-sns")))[1].click()

        # TODO - 네이버 계정 삭제

        # 프로필 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ProfileNavItems'))).click()

        # 프로필 관리 버튼 클
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'gtm-gnb-account'))).click()

        # 계정 삭제하기 변수 할당
        target = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'text-sm')))

        # 계정 삭제하기 엘리먼트 위치로 스크롤
        self.driver.execute_script('arguments[0].scrollIntoView(true);', target)

        sleep(1)

        # 계정 삭제하기 버튼 클릭
        target.click()

        sleep(1)

        # 여행을 자주 떠나지 않아서요. 라디오 버튼 클릭
        self.driver.find_element_by_id('reason_0').click()

        # 팝업의 계정 삭제하기 버튼 클릭
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-submit'))).click()

    def tearDown(self):
        self.driver.quit()