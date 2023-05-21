from pydantic import BaseModel


class BaseReservation(BaseModel):
    table_id: int
    reservation_time: str

    class Config:
        orm_mode = True


class CreateReservation(BaseReservation):
    pass


class Reservation(BaseReservation):
    id: int
    reserved_at: str
    user_id: str

