import json
import os

import pytest

from flathunter.config import Config
from flathunter.crawlers.crawl_immobilienscout import CrawlImmobilienscout
from test.crawlers.crawler_test_helpers import common_entry_assertions, common_expose_assertions

DUMMY_CONFIG = """
urls:
  - https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?numberofrooms=2.0-&price=-1500.0&livingspace=70.0-&sorting=2&pagenumber=1
    """

TEST_URL = 'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?numberofrooms=2.0-&price=-1500.0&livingspace=70.0-&sorting=2&pagenumber=1'


@pytest.fixture
def crawler():
    return CrawlImmobilienscout(Config(string=DUMMY_CONFIG))


@pytest.mark.crawler
def test_parse_exposes_from_json(crawler):
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../fixtures",
                           "immo-scout-IS24-object.json")) as fixture:
        data = json.load(fixture)
    entries = crawler.get_entries_from_json(data)
    assert len(entries) > 0


@pytest.mark.crawler
def test_crawl_works(crawler):
    entries = get_entries(crawler)
    common_entry_assertions(entries)
    assert entries[0]['url'].startswith("https://www.immobilienscout24.de/expose")


@pytest.mark.crawler
def test_process_expose_fetches_details(crawler):
    entries = get_entries(crawler)
    updated_entries = [crawler.get_expose_details(expose) for expose in entries]
    common_expose_assertions(updated_entries)


def get_entries(crawler):
    soup = crawler.get_page(TEST_URL, page_no=1)
    entries = crawler.extract_data(soup)
    return entries
