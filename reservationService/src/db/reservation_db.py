from sqlalchemy import Column, Float, Integer, String, TIMESTAMP

from src.db.database import Base


class ReservationDb(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    table_id = Column(Integer)
    user_id = Column(String)
    reservation_time = Column(Integer)
    reserved_at = Column(Integer)
