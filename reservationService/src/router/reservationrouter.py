from fastapi import APIRouter, Path, Depends, HTTPException

from reservationService.src.crud import reservation_crud
from reservationService.src.crud.reservation_crud import TableAlreadyReserved
from reservationService.src.db.database import SessionLocal, get_db
from reservationService.src.event_bus_handler import EventBusHandler
from reservationService.src.schemas.reservation_schemas import CreateReservation, Reservation

router = APIRouter()


@router.get("/tables")
def get_tables(db: SessionLocal = Depends(get_db)):
    tables = reservation_crud.get_tables(db)
    return tables


@router.get("/tables/availability")
def get_availability_tables(time: str, db: SessionLocal = Depends(get_db)):
    tables = reservation_crud.get_available_tables(db, time)
    return tables


@router.get("/tables/{table_id}")
def get_available_table(table_id: str = Path(), db: SessionLocal = Depends(get_db)):
    return {
        "table_id": table_id,
        "availability": True
    }


@router.post("/reservation", response_model=Reservation)
def post_reservation(reservation_form: CreateReservation, user_id: str,
                     db: SessionLocal = Depends(get_db), ) -> Reservation:
    ebh = EventBusHandler()
    try:
        reservation = reservation_crud.create_reservation(db, reservation_form, user_id)
    except TableAlreadyReserved:
        raise HTTPException(status_code=409, detail="Table reserved")
    ebh.publish_event(ebh.notification_channel, body={"type": "RESERVATION_CREATED"})
    return reservation


@router.delete("/reservation/{reservation_id}", status_code=202)
def get_reservation(reservation_id: int = Path(), db: SessionLocal = Depends(get_db)):
    ebh = EventBusHandler()
    reservation_crud.delete_reservation(db, reservation_id)
    ebh.publish_event(ebh.notification_channel, body={"type": "RESERVATION_CANCELLED"})
    return


@router.get("/reservation/{reservation_id}")
def get_reservation(reservation_id: int = Path(), db: SessionLocal = Depends(get_db)) -> Reservation:
    return reservation_crud.get_reservation_by_id(reservation_id, db)
