from fastapi import FastAPI, Depends

from src.crud import loyalty_crud
from src.db.database import Base, engine, get_db
from src.router import loyalty_router
from src.schemas.loyalty_schemas import Reward

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root(db=Depends(get_db)):
    loyalty_crud.add_reward(Reward(
        id=2137,
        points=21,
        date=1683221438,
        user_id=2137
    ), db)
    return {"message": "Hello World"}


app.include_router(loyalty_router.router)
