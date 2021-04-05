"""Pub/sub that does nothing. Nothing gets published, and subscribers wait forever"""
from flathunter.pubsub.pubsub import Pubsub


class NopPubsub(Pubsub):
    def publish(self, channel, string):
        pass

    def listen(self, channel):
        yield from ()
