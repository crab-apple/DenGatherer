"""Interface for webcrawlers. Crawler implementations should subclass this"""
import logging

from random_user_agent.params import HardwareType, Popularity
from random_user_agent.user_agent import UserAgent


class Headers:
    """Defines the Crawler interface"""

    __log__ = logging.getLogger('flathunt')

    _user_agent_rotator = UserAgent(popularity=[Popularity.COMMON._value_],
                                    hardware_types=[HardwareType.COMPUTER._value_])

    _headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': _user_agent_rotator.get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;'
                  'q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    @property
    def headers(self):
        return self._headers

    def rotate_user_agent(self):
        """Choose a new random user agent"""
        self._headers['User-Agent'] = self._user_agent_rotator.get_random_user_agent()
