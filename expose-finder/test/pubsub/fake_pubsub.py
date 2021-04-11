"""Pub/sub that does nothing. Nothing gets published, and subscribers wait forever"""
from flathunter.pubsub.pubsub import Pubsub


class FakePubsub(Pubsub):

    def __init__(self):
        self.__published_messages = []

    def publish(self, channel, string):
        self.__published_messages.append((channel, string))

    def listen(self, channel):
        yield from ()

    def messages(self):
        return list(self.__published_messages)


