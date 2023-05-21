import datetime

from reservationService.src.db.database import SessionLocal
from reservationService.src.db.reservation_db import ReservationDb
from reservationService.src.schemas.reservation_schemas import CreateReservation


def create_reservation(db: SessionLocal, reservation_form: CreateReservation, user_id: str):
    reserved_at = datetime.datetime.now()
    reservation_timestamp = _datetime_iso_to_timestamp(reservation_form.reservation_time)

    if len(check_availability(reservation_form.table_id, reservation_timestamp, db)) > 0:
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


def get_reservations(db: SessionLocal):
    return db.query(ReservationDb).offset(0).all()


def get_reservation_by_id(id: int, db: SessionLocal):
    return db.query(ReservationDb).filter(ReservationDb.id == id).first()


def check_availability(table_id, time, db: SessionLocal):
    tables = db.query(ReservationDb).filter(ReservationDb.table_id == table_id,
                                            ReservationDb.reservation_time.between(int(time - HOURS_2), int(time + HOURS_2))).all()
    return tables


HOURS_2 = 2 * 60 * 60


def _datetime_iso_to_timestamp(iso_time: str):
    date = datetime.datetime.fromisoformat(iso_time)
    ts = datetime.datetime.timestamp(date)
    return ts
