import json

import pika


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EventBusHandler(metaclass=Singleton):
    def __init__(self):
        self.notification_channel = None
        self.connection = None

    def publish_event(self, channel, body, routing_key='notifications', ):
        if channel is not None:
            channel.basic_publish(exchange='',
                                  routing_key=routing_key,
                                  body=json.dumps(body))
            print(" [x] Reservation sent event")

    def on_startup(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.notification_channel = self.connection.channel()
        self.notification_channel.queue_declare(queue='notifications')

    def on_shutdown(self):
        self.connection.close()
