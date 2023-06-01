import asyncio
import json
import os

import aio_pika
import pika

from src.crud.payment_crud import post_payment
from src.db.database import get_db
from src.schemas.payment_schema import CreatePayment
from utils.singleton_meta import Singleton

RABBIT_HOST = os.getenv("RABBIT_HOST")
RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PASS = os.getenv("RABBIT_PASS")


class EventBusHandler(metaclass=Singleton):
    PAYMENT_RECEIVED = "PAYMENT_RECEIVED"
    PAYMENT_REJECTED = "PAYMENT_REJECTED"

    def __init__(self):
        self.up_channel = None
        self.down_channel = None
        self.down_connection = None
        self.up_connection = None
        self.down_queue_name = 'payment'
        self.up_queue_name = 'order'

    @staticmethod
    async def on_message(message):
        async with message.process():
            message_body = json.loads(message.body)
            print(f"Message body is: {message.body}")
        event_type = str(message_body['type'])
        match event_type:
            case "ORDER_CREATED":
                db = get_db().__next__()
                post_payment(db, CreatePayment(
                    order_id=message_body["order_id"], user_id=message_body["user_id"], price=message_body["price"]
                ))

    def publish_event(self, channel, event_type, body, routing_key=None):
        if routing_key is None:
            routing_key = self.up_queue_name
        if channel is not None:
            body["type"] = event_type
            channel.basic_publish(exchange='',
                                  routing_key=routing_key,
                                  body=json.dumps(body))
            print(f" [x] {event_type} sent event")

    def publish_payment_event(self, type, payment: dict):
        self.publish_event(self.up_channel, type, payment, routing_key="order")
        self.publish_event(self.up_channel, type, payment, routing_key="loyalty")

    async def on_startup(self):
        self.up_connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST, heartbeat=0))
        self.up_channel = self.up_connection.channel()
        self.up_channel.queue_declare(queue=self.up_queue_name)
        loop = asyncio.get_event_loop()
        connection = await aio_pika.connect_robust(
            f"amqp://{RABBIT_USER}:{RABBIT_PASS}@{RABBIT_HOST}/",
            loop=loop
        )

        # Creating channel
        self.down_channel = await connection.channel()

        # Maximum message count which will be processing at the same time.
        await self.down_channel.set_qos(prefetch_count=100)

        # Declaring queue
        queue = await self.down_channel.declare_queue(self.down_queue_name, auto_delete=False, durable=True,
                                                      passive=True)

        print(" [x] Awaiting RPC requests")

        await queue.consume(self.on_message)
        self.down_connection = self.down_channel

    def on_shutdown(self):
        self.up_connection.close()
        self.down_connection.close()
