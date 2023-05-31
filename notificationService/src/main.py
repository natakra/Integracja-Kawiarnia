import asyncio
import json

import aio_pika
from fastapi import FastAPI

from src.db.database import Base, engine
from src import email_sender
from src.email_sender import EmailType

Base.metadata.create_all(bind=engine)

app = FastAPI()

channel = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def on_startup():
    global channel
    loop = asyncio.get_event_loop()
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq/",
        loop=loop
    )
    queue_name = 'notifications'

    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be processing at the same time.
    await channel.set_qos(prefetch_count=100)

    # Declaring queue
    queue = await channel.declare_queue(queue_name, auto_delete=False, durable=True, passive=True)

    async def callback(message):
        async with message.process():
            message_body = json.loads(message.body)
            print(f"Message body is: {message.body}")
        event_type = str(message_body['type'])
        email_sender.send_email(map_to_email_type(event_type), {
            "recipent": "radco.iv@gmail.com",
            "recipentName": "Radek"
        })

    print(" [x] Awaiting RPC requests")

    await queue.consume(callback)
    app.state.connection = channel


def map_to_email_type(event_type):
    if event_type == "RESERVATION_CREATED":
        return EmailType.RESERVATION_CREATED
    if event_type == "RESERVATION_CANCELLED":
        return EmailType.RESERVATION_CANCELLED
    if event_type == "MENU_UPDATED":
        return EmailType.MENU_UPDATED


@app.on_event("shutdown")
def on_shutdown():
    app.state.connection.close()
