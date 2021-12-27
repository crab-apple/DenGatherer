"""Interface for webcrawlers. Crawler implementations should subclass this"""
import logging

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CheckboxCaptchaSolver:
    __log__ = logging.getLogger('flathunt')

    def __init__(self, driver: selenium.webdriver.Chrome):
        self.driver = driver

    def resolve_captcha(self, afterlogin_string, api_key):
        self._click_captcha()

    def _click_captcha(self):
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        recaptcha_checkbox = self.driver.find_element_by_class_name("recaptcha-checkbox-checkmark")
        recaptcha_checkbox.click()
        self._wait_for_captcha_resolution()
        self.driver.switch_to.default_content()

    def _wait_for_captcha_resolution(self):
        try:
            element = WebDriverWait(self.driver, 120).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "recaptcha-checkbox-checked"))
            )
        except selenium.common.exceptions.TimeoutException:
            print("Selenium.Timeoutexception")
