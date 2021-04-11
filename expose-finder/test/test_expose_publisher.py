from flathunter.expose_publisher import ExposePublisher
from test.pubsub.fake_pubsub import FakePubsub


def test_keeps_encoding():
    pubsub = FakePubsub()
    publisher = ExposePublisher(pubsub)

    expose = {
        "title": "Möbliert"
    }
    publisher.process_expose(expose)

    published_message = pubsub.messages()[0][1]
    assert "Möbliert" in published_message
