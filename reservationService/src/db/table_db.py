from sqlalchemy import Column, Integer

from src.db.database import Base


class TableDb(Base):
    __tablename__ = "tables"

    table_id = Column(Integer, primary_key=True, index=True)
    nb_of_seats = Column(Integer)
