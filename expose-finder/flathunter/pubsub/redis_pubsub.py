import redis

from flathunter.pubsub.pubsub import Pubsub


class RedisPubsub(Pubsub):

    def __init__(self, config):
        self.redis_host = config.redis_host()
        self.redis_port = config.redis_port()

    def publish(self, channel, message):
        self.redis().publish(channel, message.encode("utf-8"))

    def listen(self, channel):
        pubsub = self.redis().pubsub()
        pubsub.subscribe(channel)
        for new_message in pubsub.listen():
            if new_message["type"] == "message" and new_message["channel"].decode("utf-8") == channel:
                data_as_string = new_message["data"].decode("utf-8")
                yield data_as_string

    def redis(self):
        return redis.Redis(self.redis_host, self.redis_port)
