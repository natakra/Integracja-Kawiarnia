import datetime
import random

from reservationService.src.db.database import SessionLocal
from reservationService.src.db.reservation_db import ReservationDb
from reservationService.src.db.table_db import TableDb
from reservationService.src.schemas.reservation_schemas import CreateReservation

HOURS_2 = 2 * 60 * 60


def _datetime_iso_to_timestamp(iso_time: str):
    date = datetime.datetime.fromisoformat(iso_time)
    ts = datetime.datetime.timestamp(date)
    return ts


def create_reservation(db: SessionLocal, reservation_form: CreateReservation, user_id: str):
    reserved_at = datetime.datetime.now()
    reservation_timestamp = _datetime_iso_to_timestamp(reservation_form.reservation_time)

    if not get_table_availability(reservation_form.table_id, reservation_timestamp, db):
        raise TableAlreadyReserved
    db_item = ReservationDb(
        table_id=reservation_form.table_id,
        user_id=user_id,
        reservation_time=reservation_timestamp,
        reserved_at=datetime.datetime.timestamp(reserved_at)
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


class TableAlreadyReserved(Exception):
    pass


def delete_reservation(db: SessionLocal, id: int):
    db.query(ReservationDb).filter(ReservationDb.id == id).delete()
    db.commit()


def get_reservations(db: SessionLocal):
    return db.query(ReservationDb).offset(0).all()


def get_reservation_by_id(id: int, db: SessionLocal):
    return db.query(ReservationDb).filter(ReservationDb.id == id).first()


def get_table_availability(table_id, time, db: SessionLocal):
    tables = db.query(ReservationDb).filter(ReservationDb.table_id == table_id,
                                            ReservationDb.reservation_time.between(int(time - HOURS_2),
                                                                                   int(time + HOURS_2))).all()
    return len(tables) == 0


def get_tables(db: SessionLocal):
    tables = db.query(TableDb).offset(0).all()
    if len(tables) == 0:
        fake_tables(db)
        tables = db.query(TableDb).offset(0).all()
    return tables


def get_available_tables(db: SessionLocal, time):
    time = _datetime_iso_to_timestamp(time)
    available_tables = [table for table in get_tables(db) if get_table_availability(table.table_id, time, db)]
    return available_tables


def fake_tables(db: SessionLocal):
    for i in range(1, 11):
        db_item = TableDb(
            table_id=i,
            nb_of_seats=random.sample([2, 3, 4, 5], 1)[0]
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
