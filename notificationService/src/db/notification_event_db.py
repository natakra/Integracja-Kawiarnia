from sqlalchemy import Column, Float, Integer, String

from src.db.database import Base


class EventDb(Base):
    __tablename__ = "notification_events"

    id = Column(String, primary_key=True, index=True)
