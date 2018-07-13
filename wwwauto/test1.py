from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import os
import time

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class mainTest(unittest.TestCase):

    def setUp(self):
        self.chromeDriver = PATH('../drivers/chromedriver')
        self.driver = webdriver.Chrome(executable_path=self.chromeDriver)
        self.wait = WebDriverWait(self.driver, 5)

    def runTest(self):
        zigbangUrl = "https://www.myrealtrip.com/offers/22565"

        self.driver.get(zigbangUrl)

        self.driver.maximize_window()

        calendarBtn = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "offer-title")))

        self.driver.execute_script("arguments[0].scrollIntoView()", calendarBtn)
        time.sleep(1)

        self.wait.until(EC.visibility_of_element_located((By.ID, "calendarBtn"))).click()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, " ui-datepicker-days-cell-over"))).click()

        self.driver.execute_script("arguments[0].scrollIntoView()", calendarBtn)
        time.sleep(1)

        self.wait.until(EC.visibility_of_element_located((By.ID, "optionBtn"))).click()

        self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".input-group-btn > button")))[1].click()

        self.wait.until(EC.visibility_of_element_located((By.ID, "checkPriceBtn"))).click()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "reserve-btn"))).click()

        time.sleep(5)


    def tearDown(self):
        self.driver.quit()