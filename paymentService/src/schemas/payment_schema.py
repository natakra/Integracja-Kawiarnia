from pydantic import BaseModel


class CreatePayment(BaseModel):
    order_id: int
    user_id: str
    price: float

    class Config:
        orm_mode = True


class Payment(CreatePayment):
    id: int
