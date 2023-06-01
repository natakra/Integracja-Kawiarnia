from pydantic import BaseModel


class Reward(BaseModel):
    id: int
    points: int
    user_id: int
    date: int

    class Config:
        orm_mode = True
