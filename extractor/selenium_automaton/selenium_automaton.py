from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class SeleniumAutomaton:
    def __init__(self):
        self.url = ''

    def connect(self, wait):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(wait)
        self.driver.get(self.url)

    def get_controls(self):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError

    def click_delay(self, element, long):
        element.click()
        time.sleep(long)

    def switch_to_frame(self, xpath):
        wait = WebDriverWait(self.driver, 100)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))