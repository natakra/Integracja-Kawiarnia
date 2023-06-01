from sqlalchemy import Column, Integer, String

from src.db.database import Base


class Coffees(Base):
    __tablename__ = "freecoffees"
    user_id = Column(String, primary_key=True)
    free_coffees = Column(Integer)
