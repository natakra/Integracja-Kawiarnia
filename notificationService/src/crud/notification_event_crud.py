from src.db.database import SessionLocal
from src.db.notification_event_db import EventDb
from src.schemas.notification_event import Event


def get_all_items(db: SessionLocal):
    return db.query(EventDb).offset(0).all()


def add_new_item(new_item: Event, db: SessionLocal):
    db_item = EventDb(id=new_item.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(id: int, db: SessionLocal):
    return db.query(EventDb).filter(EventDb.id == id).first()
