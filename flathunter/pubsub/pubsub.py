"""Defines the interface for the pub/sub service"""


class Pubsub:
    def publish(self, channel, string):
        pass

    def listen(self, channel):
        pass
