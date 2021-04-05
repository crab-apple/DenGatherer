import json
import logging

import redis

from flathunter.abstract_processor import Processor


class ExposePublisher(Processor):
    """Expose processor that publishes them to the pub/sub system"""
    __log__ = logging.getLogger('flathunt')

    def __init__(self, config):
        self.config = config

    def process_expose(self, expose):
        r = redis.Redis(self.config.redis_host(), self.config.redis_port())
        r.publish("exposes", json.dumps(expose))
        return expose
