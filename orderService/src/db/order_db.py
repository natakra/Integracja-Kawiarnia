from sqlalchemy import Column, Float, Integer, String, Boolean

from src.db.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String)
    price = Column(Float)
    # free_coffees = Column(Integer)
    status = Column(String)
