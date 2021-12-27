"""Interface for webcrawlers. Crawler implementations should subclass this"""
import logging
from time import sleep as sleep

import requests
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CaptchaSolver:
    __log__ = logging.getLogger('flathunt')

    def __init__(self, driver: selenium.webdriver.Chrome):
        self.driver = driver

    def resolve_captcha(self, afterlogin_string, api_key):
        iframe_present = self._check_if_iframe_visible()
        if afterlogin_string == "" and iframe_present:
            self._solve(api_key)
        else:
            self._wait_for_captcha_resolution(afterlogin_string)

    def _check_if_iframe_not_visible(self):
        try:
            iframe = WebDriverWait(self.driver, 10).until(EC.invisibility_of_element(
                (By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor?']")))
            return iframe
        except NoSuchElementException:
            print("Element not found")

    def _check_if_iframe_visible(self):
        try:
            iframe = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor?']")))
            return iframe
        except NoSuchElementException:
            print("No iframe found, therefore no chaptcha verification necessary")

    def _wait_for_captcha_resolution(self, afterlogin_string=""):
        xpath_string = f"//*[contains(text(), '{afterlogin_string}')]"
        try:
            element = WebDriverWait(self.driver, 120).until(
                EC.visibility_of_element_located((By.XPATH, xpath_string)))
        except selenium.common.exceptions.TimeoutException:
            print("Selenium.Timeoutexception")

    def _solve(self, api_key):
        google_site_key = self.driver.find_element_by_class_name("g-recaptcha").get_attribute("data-sitekey")
        self.__log__.debug("Google site key: %s", google_site_key)
        url = self.driver.current_url
        session = requests.Session()
        postrequest = (
            f"http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={google_site_key}&pageurl={url}"
        )
        captcha_id = session.post(postrequest).text.split("|")[1]
        recaptcha_answer = session.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}").text
        while "CAPCHA_NOT_READY" in recaptcha_answer:
            sleep(5)
            self.__log__.debug("Captcha status: %s", recaptcha_answer)
            recaptcha_answer = session.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}").text
        self.__log__.debug("Captcha promise: %s", recaptcha_answer)
        recaptcha_answer = recaptcha_answer.split("|")[1]
        self.driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{recaptcha_answer}";')
        # TODO: Below function call can be different depending on the websites implementation. It is responsible for
        #  sending the the promise that we get from recaptcha_answer. For now, if it breaks, it is required to
        #  reverse engineer it by hand. Not sure if there is a way to automate it.
        self.driver.execute_script(f'solvedCaptcha("{recaptcha_answer}")')
        self._check_if_iframe_not_visible()
