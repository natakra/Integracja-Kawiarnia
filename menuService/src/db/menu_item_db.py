from sqlalchemy import Column, Float, Integer, String

from src.db.database import Base


class MenuItem(Base):
    __tablename__ = "menuitems"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float)
