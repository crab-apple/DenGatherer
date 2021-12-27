"""Interface for webcrawlers. Crawler implementations should subclass this"""
from time import sleep as sleep

import requests
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def _check_if_iframe_not_visible(driver: selenium.webdriver.Chrome):
    try:
        iframe = WebDriverWait(driver, 10).until(EC.invisibility_of_element(
            (By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor?']")))
        return iframe
    except NoSuchElementException:
        print("Element not found")


def _check_if_iframe_visible(driver: selenium.webdriver.Chrome):
    try:
        iframe = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor?']")))
        return iframe
    except NoSuchElementException:
        print("No iframe found, therefore no chaptcha verification necessary")


def _wait_for_captcha_resolution(driver, checkbox: bool, afterlogin_string=""):
    if checkbox:
        try:
            element = WebDriverWait(driver, 120).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "recaptcha-checkbox-checked"))
            )
        except selenium.common.exceptions.TimeoutException:
            print("Selenium.Timeoutexception")
    else:
        xpath_string = f"//*[contains(text(), '{afterlogin_string}')]"
        try:
            element = WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_string)))
        except selenium.common.exceptions.TimeoutException:
            print("Selenium.Timeoutexception")


def _clickcaptcha(driver, checkbox: bool):
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    recaptcha_checkbox = driver.find_element_by_class_name("recaptcha-checkbox-checkmark")
    recaptcha_checkbox.click()
    _wait_for_captcha_resolution(driver, checkbox)
    driver.switch_to.default_content()


def _solve(driver, api_key, logger):
    google_site_key = driver.find_element_by_class_name("g-recaptcha").get_attribute("data-sitekey")
    logger.debug("Google site key: %s", google_site_key)
    url = driver.current_url
    session = requests.Session()
    postrequest = (
        f"http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={google_site_key}&pageurl={url}"
    )
    captcha_id = session.post(postrequest).text.split("|")[1]
    recaptcha_answer = session.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}").text
    while "CAPCHA_NOT_READY" in recaptcha_answer:
        sleep(5)
        logger.debug("Captcha status: %s", recaptcha_answer)
        recaptcha_answer = session.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}").text
    logger.debug("Captcha promise: %s", recaptcha_answer)
    recaptcha_answer = recaptcha_answer.split("|")[1]
    driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{recaptcha_answer}";')
    # TODO: Below function call can be different depending on the websites implementation. It is responsible for
    #  sending the the promise that we get from recaptcha_answer. For now, if it breaks, it is required to
    #  reverse engineer it by hand. Not sure if there is a way to automate it.
    driver.execute_script(f'solvedCaptcha("{recaptcha_answer}")')
    _check_if_iframe_not_visible(driver)


def resolve_captcha(driver, checkbox: bool, afterlogin_string, api_key, logger):
    iframe_present = _check_if_iframe_visible(driver)
    if checkbox is False and afterlogin_string == "" and iframe_present:
        _solve(driver, api_key, logger)
    else:
        if checkbox:
            _clickcaptcha(driver, checkbox)
        else:
            _wait_for_captcha_resolution(driver, checkbox, afterlogin_string)
