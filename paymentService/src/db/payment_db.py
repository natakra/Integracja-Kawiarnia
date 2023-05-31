from sqlalchemy import Column, Float, Integer, String

from src.db.database import Base


class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer)
    user_id = Column(String)
    price = Column(Float)
