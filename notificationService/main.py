import asyncio

import aio_pika
from fastapi import FastAPI

from menuService.src.db.database import Base, engine

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
        loop=loop
    )
    queue_name = 'notifications'

    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be processing at the same time.
    await channel.set_qos(prefetch_count=100)

    # Declaring queue
    queue = await channel.declare_queue(queue_name, auto_delete=False, durable=True, passive=True)

    def callback(body):
        print(" [x] Received %r" % body)

    print(" [x] Awaiting RPC requests")

    await queue.consume(callback=callback)
    app.state.connection = channel


@app.on_event("shutdown")
def on_shutdown():
    app.state.connection.close()
