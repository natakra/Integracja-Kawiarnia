from fastapi import FastAPI

from src.db.database import Base, engine
from src.event_bus_handler import EventBusHandler
from src.router import orderrouter

Base.metadata.create_all(bind=engine)

app = FastAPI()
ebh: EventBusHandler | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(orderrouter.router)


@app.on_event("startup")
async def on_startup():
    global ebh
    ebh = EventBusHandler()
    await ebh.on_startup()


@app.on_event("shutdown")
async def on_shutdown():
    ebh.on_shutdown()


def get_ebh():
    return ebh
