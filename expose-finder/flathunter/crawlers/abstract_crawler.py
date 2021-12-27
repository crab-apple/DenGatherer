"""Interface for webcrawlers. Crawler implementations should subclass this"""
import logging
import re

import requests
from bs4 import BeautifulSoup
from random_user_agent.params import HardwareType, Popularity
from random_user_agent.user_agent import UserAgent

from flathunter import proxies
from flathunter.crawlers.captcha.captchasolvers import get_captcha_solver


class Crawler:
    """Defines the Crawler interface"""

    __log__ = logging.getLogger('flathunt')
    URL_PATTERN = None

    def __init__(self, config):
        self.config = config

    user_agent_rotator = UserAgent(popularity=[Popularity.COMMON._value_],
                                   hardware_types=[HardwareType.COMPUTER._value_])

    HEADERS = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent_rotator.get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;'
                  'q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    def rotate_user_agent(self):
        """Choose a new random user agent"""
        self.HEADERS['User-Agent'] = self.user_agent_rotator.get_random_user_agent()

    # pylint: disable=unused-argument
    def get_page(self, search_url, driver=None, page_no=None):
        """Applies a page number to a formatted search URL and fetches the exposes at that page"""
        return self.get_soup_from_url(search_url)

    def get_soup_from_url(self, url, driver=None, captcha_api_key=None, checkbox=None, afterlogin_string=None):
        """Creates a Soup object from the HTML at the provided URL"""

        self.rotate_user_agent()
        resp = requests.get(url, headers=self.HEADERS)
        if resp.status_code != 200:
            self.__log__.error("Got response (%i): %s", resp.status_code, resp.content)
        if self.config.use_proxy():
            return self.get_soup_with_proxy(url)
        if driver is not None:
            driver.get(url)
            if re.search("g-recaptcha", driver.page_source):
                get_captcha_solver(driver, checkbox).resolve_captcha(afterlogin_string, captcha_api_key)
            return BeautifulSoup(driver.page_source, 'html.parser')
        return BeautifulSoup(resp.content, 'html.parser')

    def get_soup_with_proxy(self, url):
        """Will try proxies until it's possible to crawl and return a soup"""
        resolved = False
        resp = None

        # We will keep trying to fetch new proxies until one works
        while not resolved:
            proxies_list = proxies.get_proxies()
            for proxy in proxies_list:
                self.rotate_user_agent()

                try:
                    # Very low proxy read timeout, or it will get stuck on slow proxies
                    resp = requests.get(url, headers=self.HEADERS, proxies={"http": proxy, "https": proxy},
                                        timeout=(20, 0.1))

                    if resp.status_code != 200:
                        self.__log__.error("Got response (%i): %s", resp.status_code, resp.content)
                    else:
                        resolved = True
                        break

                except requests.exceptions.ConnectionError:
                    self.__log__.error("Connection failed for proxy %s. Trying new proxy...", proxy)
                except requests.exceptions.Timeout:
                    self.__log__.error("Connection timed out for proxy %s. Trying new proxy...", proxy)
                except:
                    self.__log__.error("Some error occurred. Trying new proxy...")

        if not resp:
            raise Exception("An error occurred while fetching proxies or content")

        return BeautifulSoup(resp.content, 'html.parser')

    # pylint: disable=no-self-use
    def extract_data(self, soup):
        """Should be implemented in subclass"""
        raise Exception("Method not implemented")

    # pylint: disable=unused-argument
    def get_results(self, search_url, max_pages=None):
        """Loads the exposes from the site, starting at the provided URL"""
        self.__log__.debug("Got search URL %s", search_url)

        # load first page
        soup = self.get_page(search_url)

        # get data from first page
        entries = self.extract_data(soup)
        self.__log__.debug('Number of found entries: %d', len(entries))

        return entries

    def crawl(self, url, max_pages=None):
        """Load as many exposes as possible from the provided URL"""
        if re.search(self.URL_PATTERN, url):
            try:
                return self.get_results(url, max_pages)
            except requests.exceptions.ConnectionError:
                self.__log__.warning("Connection to %s failed. Retrying.", url.split('/')[2])
                return []
        return []

    def get_name(self):
        """Returns the name of this crawler"""
        return type(self).__name__

    def get_expose_details(self, expose):
        """Loads additional details for an expose. Should be implemented in the subclass"""
        return expose
