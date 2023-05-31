from fastapi import APIRouter, Depends

from src.crud.order_crud import create_order
from src.db.database import get_db, SessionLocal
from src.dependencies import get_ebh
from src.event_bus_handler import EventBusHandler
from src.schemas.order_schemas import Order, CreateOrder

router = APIRouter()


@router.post("/order", response_model=Order)
def post_order(order_form: CreateOrder, user_id: str, db: SessionLocal = Depends(get_db),
               ebh: EventBusHandler = Depends(get_ebh)) -> Order:
    order: Order = create_order(db, order_form, user_id)
    ebh.publish_order_event(order={"user_id": order.user_id, "order_id": order.id, "price": order.price})
    return order
