"""Functions and classes related to sending Telegram messages"""
import json
import logging
import urllib.error
import urllib.parse
import urllib.request

import requests

from flathunter.pubsub.redis_pubsub import RedisPubsub


class SenderTelegram:
    """Expose processor that sends Telegram messages"""
    __log__ = logging.getLogger('flathunt')

    exposes_channel = "exposes"

    def __init__(self, config, receivers=None):
        self.config = config
        self.pubsub = RedisPubsub(config)
        self.bot_token = self.config.get('telegram', dict()).get('bot_token', '')
        if receivers is None:
            self.receiver_ids = self.config.get('telegram', dict()).get('receiver_ids', list())
        else:
            self.receiver_ids = receivers

    def wait_and_process(self):
        for new_message in self.pubsub.listen(self.exposes_channel):
            expose = json.loads(new_message)
            self.process_expose(expose)

    def process_expose(self, expose):
        """Send a message to a user describing the expose"""
        message = self.config.get('message', "").format(
            title=expose['title'],
            rooms=expose['rooms'],
            size=expose['size'],
            price=expose['price'],
            url=expose['url'],
            address=expose['address'],
            durations="" if 'durations' not in expose else expose['durations']).strip()
        self.send_msg(message)

    def send_msg(self, message):
        """Send messages to each of the receivers in receiver_ids"""
        if self.receiver_ids is None:
            return
        for chat_id in self.receiver_ids:
            url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%i&text=%s'
            text = urllib.parse.quote_plus(message.encode('utf-8'))
            self.__log__.debug(('token:', self.bot_token))
            self.__log__.debug(('chatid:', chat_id))
            self.__log__.debug(('text', text))
            qry = url % (self.bot_token, chat_id, text)
            self.__log__.debug("Retrieving URL %s", qry)
            resp = requests.get(qry)
            self.__log__.debug("Got response (%i): %s", resp.status_code, resp.content)
            data = resp.json()

            # handle error
            if resp.status_code != 200:
                status_code = resp.status_code
                self.__log__.error("When sending bot message, we got status %i with message: %s",
                                   status_code, data)
