from pydantic import BaseModel


class Event(BaseModel):
    id: str

    class Config:
        orm_mode = True
