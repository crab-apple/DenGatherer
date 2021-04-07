#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Flathunter - search for flats by crawling property portals, and receive telegram
   messages about them. This is the main command-line executable, for running on the
   console."""

import argparse
import logging
import os
from pprint import pformat

from flathunter.config import Config

__author__ = "Jan Harrie"
__version__ = "1.0"
__maintainer__ = "Nody"
__email__ = "harrymcfly@protonmail.com"
__status__ = "Production"

# init logging
from flathunter.pubsub.redis_pubsub import RedisPubsub
from flathunter.sender_telegram import SenderTelegram

if os.name == 'posix':
    # coloring on linux
    CYELLOW = '\033[93m'
    CBLUE = '\033[94m'
    COFF = '\033[0m'
    LOG_FORMAT = '[' + CBLUE + '%(asctime)s' + COFF + '|' + CBLUE + '%(filename)-18s' + COFF + \
                 '|' + CYELLOW + '%(levelname)-8s' + COFF + ']: %(message)s'
else:
    # else without color
    LOG_FORMAT = '[%(asctime)s|%(filename)-18s|%(levelname)-8s]: %(message)s'
logging.basicConfig(
    format=LOG_FORMAT,
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO)
__log__ = logging.getLogger('flathunt')


def main():
    """Processes command-line arguments, loads the config, launches the flathunter"""
    parser = argparse.ArgumentParser(description= \
                                         "Searches for flats on Immobilienscout24.de and wg-gesucht.de and sends " + \
                                         "results to Telegram User", epilog="Designed by Nody")
    parser.add_argument('--config', '-c',
                        type=argparse.FileType('r', encoding='UTF-8'),
                        default='%s/config.yaml' % os.path.dirname(os.path.abspath(__file__)),
                        help="Config file to use. If not set, try to use '%s/config.yaml' " %
                             os.path.dirname(os.path.abspath(__file__))
                        )
    args = parser.parse_known_args()[0]

    # load config
    config_handle = args.config
    config = Config(config_handle.name)

    # check config
    if not config.get('telegram', dict()).get('bot_token'):
        __log__.error("No telegram bot token configured. Starting like this would be pointless...")
        return
    if not config.get('telegram', dict()).get('receiver_ids'):
        __log__.warning("No telegram receivers configured - nobody will get notifications.")

    # adjust log level, if required
    if config.get('verbose'):
        __log__.setLevel(logging.DEBUG)
        __log__.debug("Settings from config: %s", pformat(config))

    # start sending messages
    telegram_sender = SenderTelegram(config, RedisPubsub(config))
    telegram_sender.wait_and_process()


if __name__ == "__main__":
    main()
