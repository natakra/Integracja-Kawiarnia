from fastapi import FastAPI, Depends

from src.db.database import Base, engine, get_db
from src.event_bus_handler import EventBusHandler
from src.router import loyalty_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

ebh = EventBusHandler()


@app.get("/")
async def root(user_id: str, db=Depends(get_db)):
    ebh.send_update(db, user_id=user_id)
    return {"message": "Hello World"}


app.include_router(loyalty_router.router)


@app.on_event("startup")
async def on_startup():
    global ebh
    ebh = EventBusHandler()
    await ebh.on_startup()


@app.on_event("shutdown")
def on_shutdown():
    ebh.on_shutdown()
