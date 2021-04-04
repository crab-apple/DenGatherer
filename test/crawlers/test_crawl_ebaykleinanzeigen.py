import pytest

from flathunter.config import Config
from flathunter.crawlers.crawl_ebaykleinanzeigen import CrawlEbayKleinanzeigen
from test.crawlers.crawler_test_helpers import common_entry_assertions, common_expose_assertions

DUMMY_CONFIG = """
urls:
  - https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/muenchen/anbieter:privat/anzeige:angebote/preis:600:1000
    """

TEST_URL = 'https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/preis:1000:1500/c203l3331+wohnung_mieten.qm_d:70,+wohnung_mieten.zimmer_d:2'


@pytest.fixture
def crawler():
    return CrawlEbayKleinanzeigen(Config(string=DUMMY_CONFIG))


@pytest.mark.crawler
def test_crawler(crawler):
    entries = get_entries(crawler)
    common_entry_assertions(entries)
    assert entries[0]['url'].startswith("https://www.ebay-kleinanzeigen.de/s-anzeige")


@pytest.mark.crawler
def test_process_expose_fetches_details(crawler):
    entries = get_entries(crawler)
    updated_entries = [crawler.get_expose_details(expose) for expose in entries]
    common_expose_assertions(updated_entries)


def get_entries(crawler):
    soup = crawler.get_page(TEST_URL)
    entries = crawler.extract_data(soup)
    return entries
