import pytest

from flathunter.config import Config
from flathunter.crawlers.crawl_immowelt import CrawlImmowelt
from test.crawlers.crawler_test_helpers import common_entry_assertions, assert_common_attribute, \
    common_expose_assertions
from test.test_util import count

DUMMY_CONFIG = """
urls:
  - https://www.immowelt.de/liste/muenchen/wohnungen/mieten?roomi=2&primi=600&prima=1000
    """

TEST_URL = 'https://www.immowelt.de/liste/berlin/wohnungen/mieten?roomi=2&prima=1500&wflmi=70&sort=createdate%2Bdesc'


@pytest.fixture
def crawler():
    return CrawlImmowelt(Config(string=DUMMY_CONFIG))


@pytest.mark.crawler
def test_crawler(crawler):
    entries = get_entries(crawler)
    common_entry_assertions(entries)

    assert entries[0]['url'].startswith("https://www.immowelt.de/expose")

    # We don't check that all listings have an image, as sometimes some don't.
    # However, let's check that at least one has an image to make sure that this part
    # isn't broken.
    assert_common_attribute("image", entries)


@pytest.mark.crawler
def test_dont_crawl_other_urls(crawler):
    exposes = crawler.crawl("https://www.example.com")
    assert count(exposes) == 0


@pytest.mark.crawler
def test_process_expose_fetches_details(crawler):
    entries = get_entries(crawler)
    updated_entries = [crawler.get_expose_details(expose) for expose in entries]
    common_expose_assertions(updated_entries)


def get_entries(crawler):
    soup = crawler.get_page(TEST_URL)
    entries = crawler.extract_data(soup)
    return entries
