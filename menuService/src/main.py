from fastapi import FastAPI

import src.router.menurouter as menurouter
from src.event_bus_handler import EventBusHandler
from src.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
ebh: EventBusHandler | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(menurouter.router)


@app.on_event("startup")
def on_startup():
    global ebh
    ebh = EventBusHandler()
    ebh.on_startup()


@app.on_event("shutdown")
def on_shutdown():
    ebh.on_shutdown()


