import json
import os

import pika

from utils.singleton_meta import Singleton

RABBIT_HOST = os.getenv("RABBIT_HOST")
RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PASS = os.getenv("RABBIT_PASS")


class EventBusHandler(metaclass=Singleton):
    def __init__(self):
        self.notification_channel = None
        self.connection = None

    def publish_event(self, channel, body, routing_key='notifications'):
        if channel is not None:
            channel.basic_publish(exchange='',
                                  routing_key=routing_key,
                                  body=json.dumps(body))
            print(" [x] Reservation sent event")

    def on_startup(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST, heartbeat=0))
        self.notification_channel = self.connection.channel()
        self.notification_channel.queue_declare(queue='notifications')

    def on_shutdown(self):
        self.connection.close()
