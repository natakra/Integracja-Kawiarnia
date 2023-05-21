from sqlalchemy import Column, Integer, String, Boolean

from reservationService.src.db.database import Base


class TableDb(Base):
    __tablename__ = "tables"

    table_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    availability = Column(Boolean)
    nb_of_seats = Column(Integer)
