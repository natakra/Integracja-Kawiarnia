import asyncio
import json
import os

import aio_pika
import pika

# from src.crud.order_crud import update_menu, order_status_update
# from src.schemas.order_schemas import OrderStatus
from src.crud import loyalty_crud
from src.crud.loyalty_crud import collect_reward
from src.db.database import get_db
from utils.singleton_meta import Singleton

RABBIT_HOST = os.getenv("RABBIT_HOST")
RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PASS = os.getenv("RABBIT_PASS")


class EventBusHandler(metaclass=Singleton):
    LOYALTY_POINTS = "USER_POINTS"

    def __init__(self):
        self.up_channel = None
        self.down_channel = None
        self.down_connection = None
        self.up_connection = None
        self.up_queue_name = 'order'
        self.down_queue_name = 'loyalty'

    async def on_message(self, message):
        db = get_db().__next__()
        async with message.process():
            message_body = json.loads(message.body)
            print(f"Message body is: {message.body}")
        event_type = str(message_body['type'])
        match event_type:
            case "ORDER_CREATED":
                self.handle_order_created(db, message_body)
            case "PAYMENT_RECEIVED":
                self.handle_payment_received(db, message_body)

    def publish_event(self, channel, event_type, body, routing_key=None):
        if routing_key is None:
            routing_key = self.up_queue_name
        if channel is not None:
            body["type"] = event_type
            channel.basic_publish(exchange='',
                                  routing_key=routing_key,
                                  body=json.dumps(body))
            print(f" [x] {event_type} sent event")

    def publish_points_event(self, points: dict):
        self.publish_event(self.up_channel, EventBusHandler.LOYALTY_POINTS, points)

    async def on_startup(self):
        self.up_connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST, heartbeat=0))
        self.up_channel = self.up_connection.channel()
        self.up_channel.queue_declare(queue=self.up_queue_name)

        loop = asyncio.get_event_loop()
        down_connection = await aio_pika.connect_robust(
            f"amqp://{RABBIT_USER}:{RABBIT_PASS}@{RABBIT_HOST}/",
            loop=loop
        )

        # Creating channel
        self.down_channel = await down_connection.channel()

        # Maximum message count which will be processing at the same time.
        await self.down_channel.set_qos(prefetch_count=100)

        # Declaring queue
        queue = await self.down_channel.declare_queue(self.down_queue_name, auto_delete=False, durable=True,
                                                      passive=True)

        print(" [x] Awaiting RPC requests")

        await queue.consume(self.on_message)
        self.down_connection = self.down_channel

    def on_shutdown(self):
        self.down_connection.close()
        self.up_connection.close()

    def handle_order_created(self, db, event):
        points_to_collect = 100 * event["free_coffee_count"]
        user_id = event["user_id"]
        collect_reward(points_to_collect, user_id, db)
        self.send_update(db, user_id)

    def handle_payment_received(self, db, event):
        price = int(event["price"])
        user_id = event["user_id"]
        loyalty_crud.add_reward(user_id, price, db)
        self.send_update(db, user_id)

    def send_update(self, db, user_id):
        self.publish_points_event({
            "user_id": user_id,
            "points": loyalty_crud.get_points(user_id, db)
        })
