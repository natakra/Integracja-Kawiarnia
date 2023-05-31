import pika
from fastapi import FastAPI

from src.db.database import engine, Base
from src.event_bus_handler import EventBusHandler
from src.router.reservationrouter import router

app = FastAPI()

event_bus_handler = EventBusHandler()
Base.metadata.create_all(bind=engine)


@app.get('/')
def root():
    return {"message": "Hello World"}


app.include_router(router)


@app.on_event("startup")
def on_startup():
    event_bus_handler.on_startup()


@app.on_event("shutdown")
def on_shutdown():
    event_bus_handler.on_shutdown()
