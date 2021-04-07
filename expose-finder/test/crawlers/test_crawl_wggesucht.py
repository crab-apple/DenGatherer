import unittest

import pytest

from flathunter.config import Config
from flathunter.crawlers.crawl_wggesucht import CrawlWgGesucht
from test.crawlers.crawler_test_helpers import assert_required_attribute, assert_common_attribute, \
    common_entry_assertions


@pytest.mark.crawler
class WgGesuchtCrawlerTest(unittest.TestCase):
    TEST_URL = 'https://www.wg-gesucht.de/wohnungen-in-Berlin.8.2.1.0.html?offer_filter=1&city_id=8&noDeact=1&categories%5B%5D=2&rent_types%5B%5D=0&sMin=70&rMax=1500&rmMin=2&fur=2&sin=2&exc=2&img_only=1'
    DUMMY_CONFIG = """
    urls:
      - https://www.wg-gesucht.de/wohnungen-in-Munchen.90.2.1.0.html
        """

    def setUp(self):
        self.crawler = CrawlWgGesucht(Config(string=self.DUMMY_CONFIG))

    def test(self):
        soup = self.crawler.get_page(self.TEST_URL)
        self.assertIsNotNone(soup, "Should get a soup from the URL")
        entries = self.crawler.extract_data(soup)

        common_entry_assertions(entries)
        assert_required_attribute("from", entries)
        assert_common_attribute("to", entries)

        self.assertTrue(entries[0]['url'].startswith("https://www.wg-gesucht.de/wohnungen"),
                        u"URL should be an apartment link")
