from fastapi import APIRouter, Depends

from src.crud import loyalty_crud
from src.db.database import get_db

router = APIRouter()


@router.get("/loyalty/points")
async def get_points(user_id: str, db = Depends(get_db)):
    print(loyalty_crud.get_points(user_id, db))
    return loyalty_crud.get_points(user_id, db)


@router.get("/loyalty/activetransactions")
async def get_all_active_rewards(user_id: str, db = Depends(get_db)):
    return loyalty_crud.get_active_rewards(user_id, db)
