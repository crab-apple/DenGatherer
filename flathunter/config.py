"""Wrap configuration options as an object"""
import logging
import os

import yaml

from flathunter.crawlers.crawl_ebaykleinanzeigen import CrawlEbayKleinanzeigen
from flathunter.crawlers.crawl_idealista import CrawlIdealista
from flathunter.crawlers.crawl_immobiliare import CrawlImmobiliare
from flathunter.crawlers.crawl_immobilienscout import CrawlImmobilienscout
from flathunter.crawlers.crawl_immowelt import CrawlImmowelt
from flathunter.crawlers.crawl_wggesucht import CrawlWgGesucht
from flathunter.crawlers.crawler_subito import CrawlSubito
from flathunter.filter import Filter


class Config:
    """Class to represent flathunter configuration"""

    __log__ = logging.getLogger('flathunt')

    def __init__(self, filename=None, string=None):
        if string is not None:
            self.config = yaml.safe_load(string)
        else:
            if filename is None:
                filename = os.path.dirname(os.path.abspath(__file__)) + "/../config.yaml"
            self.__log__.info("Using config %s", filename)
            with open(filename) as file:
                self.config = yaml.safe_load(file)
        self.__searchers__ = [CrawlImmobilienscout(self),
                              CrawlWgGesucht(self),
                              CrawlEbayKleinanzeigen(self),
                              CrawlImmowelt(self),
                              CrawlSubito(self),
                              CrawlImmobiliare(self),
                              CrawlIdealista(self)]

    def __iter__(self):
        """Emulate dictionary"""
        return self.config.__iter__()

    def __getitem__(self, value):
        """Emulate dictionary"""
        return self.config[value]

    def get(self, key, value=None):
        """Emulate dictionary"""
        return self.config.get(key, value)

    def database_location(self):
        """Return the location of the database folder"""
        if "database_location" in self.config:
            return self.config["database_location"]
        return os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..")

    def set_searchers(self, searchers):
        """Update the active search plugins"""
        self.__searchers__ = searchers

    def searchers(self):
        """Get the list of search plugins"""
        return self.__searchers__

    def get_filter(self):
        """Read the configured filter"""
        builder = Filter.builder()
        builder.read_config(self.config)
        return builder.build()

    def captcha_enabled(self):
        return ("captcha" in self.config)

    def use_proxy(self):
        return ("use_proxy_list" in self.config and self.config["use_proxy_list"])
