import json
import logging

from flathunter.abstract_processor import Processor
from flathunter.pubsub.redis_pubsub import RedisPubsub


class ExposePublisher(Processor):
    """Expose processor that publishes them to the pub/sub system"""
    __log__ = logging.getLogger('flathunt')

    def __init__(self, config):
        self.pubsub = RedisPubsub(config)

    def process_expose(self, expose):
        self.pubsub.publish("exposes", json.dumps(expose))
        return expose
