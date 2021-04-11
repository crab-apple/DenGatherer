import json
import logging

from flathunter.abstract_processor import Processor


class ExposePublisher(Processor):
    """Expose processor that publishes them to the pub/sub system"""
    __log__ = logging.getLogger('flathunt')

    def __init__(self, pubsub):
        self.pubsub = pubsub

    def process_expose(self, expose):
        self.pubsub.publish("exposes", json.dumps(expose, ensure_ascii=False))
        return expose
