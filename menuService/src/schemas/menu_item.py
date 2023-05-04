from pydantic import BaseModel


class MenuItem(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True


class MenuItemCreate(BaseModel):
    name: str
    price: float

    class Config:
        orm_mode = True
