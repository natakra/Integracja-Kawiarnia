from fastapi import FastAPI

import menuService.src.router.menurouter as menurouter
from menuService.src.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(menurouter.router)
