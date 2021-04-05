"""Defines the interface for the pub/sub service"""


class Pubsub:
    def publish(self, channel, string):
        raise NotImplementedError()

    def listen(self, channel):
        raise NotImplementedError()
