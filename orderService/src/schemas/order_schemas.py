from enum import Enum
from typing import List

from pydantic import BaseModel


class OrderStatus(Enum):
    STATUS_ACCEPTED = "accepted"
    STATUS_PAID = "paid"
    STATUS_CANCELLED = "cancelled"
    STATUS_DONE = "done"


class CreateOrder(BaseModel):
    product_ids: List[int]

    class Config:
        orm_mode = True


class Order(BaseModel):
    user_id: str
    id: int
    price: float
    status: OrderStatus

    class Config:
        orm_mode = True
