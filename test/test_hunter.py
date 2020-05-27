import unittest
import yaml
from flathunter.crawl_immowelt import CrawlImmowelt
from flathunter.hunter import Hunter 
from flathunter.config import Config
from flathunter.idmaintainer import IdMaintainer

class HunterTest(unittest.TestCase):

    DUMMY_CONFIG = """
urls:
  - https://www.immowelt.de/liste/berlin/wohnungen/mieten?roomi=2&prima=1500&wflmi=70&sort=createdate%2Bdesc

google_maps_api:
  key: SOME_KEY
  url: https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={dest}&mode={mode}&sensor=true&key={key}&arrival_time={arrival}
  enable: true
    """

    def setUp(self):
        self.hunter = Hunter(Config(string=self.DUMMY_CONFIG), [CrawlImmowelt()], IdMaintainer(":memory:"))

    def test_hunt_flats(self):
        exposes = self.hunter.hunt_flats()
        self.assertTrue(len(exposes) > 0, "Expected to find exposes")