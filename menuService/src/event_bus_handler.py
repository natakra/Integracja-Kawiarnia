import json
import os
from typing import List

import pika

from utils.singleton_meta import Singleton

RABBIT_HOST = os.getenv("RABBIT_HOST")
RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PASS = os.getenv("RABBIT_PASS")


class EventBusHandler(metaclass=Singleton):
    MENU_UPDATED_TYPE = "MENU_UPDATED"

    def __init__(self):
        self.channel = None
        self.connection = None
        self.queue_name = "order"

    def publish_event(self, channel, event_type, body, routing_key=None):
        if routing_key is None:
            routing_key = self.queue_name
        if channel is not None:
            body["type"] = event_type
            channel.basic_publish(exchange='',
                                  routing_key=routing_key,
                                  body=json.dumps(body))
            print(f" [x] {event_type} sent event")

    def publish_menu_update_event(self, new_menu: List[dict]):
        self.publish_event(self.channel, EventBusHandler.MENU_UPDATED_TYPE, {
            "menu_update": new_menu
        })

    def on_startup(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST, heartbeat=0))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def on_shutdown(self):
        self.connection.close()
