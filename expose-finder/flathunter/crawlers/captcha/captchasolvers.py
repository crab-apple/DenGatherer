"""Interface for webcrawlers. Crawler implementations should subclass this"""

import selenium
from selenium import webdriver

from flathunter.crawlers.captcha.captchasolver import CaptchaSolver
from flathunter.crawlers.captcha.checkboxcaptchasolver import CheckboxCaptchaSolver


def get_captcha_solver(driver: selenium.webdriver.Chrome, checkbox: bool):
    if checkbox:
        return CheckboxCaptchaSolver(driver)
    else:
        return CaptchaSolver(driver)
