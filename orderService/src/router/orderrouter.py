from fastapi import APIRouter, Depends

from src.crud.order_crud import create_order, order_status_update, how_many_coffees_discount
from src.db.database import get_db, SessionLocal
from src.dependencies import get_ebh
from src.event_bus_handler import EventBusHandler
from src.schemas.order_schemas import Order, CreateOrder

router = APIRouter()


@router.post("/order", response_model=Order)
def post_order(order_form: CreateOrder, user_id: str, db: SessionLocal = Depends(get_db),
               ebh: EventBusHandler = Depends(get_ebh)) -> Order:
    order: Order = create_order(db, order_form, user_id)

    coffee_discount, free_coffees_count = how_many_coffees_discount(db, order_form.product_ids, user_id)
    print(coffee_discount)
    print(free_coffees_count)
    ebh.publish_order_to_loyalty_event(order={"user_id": order.user_id, "order_id": order.id,
                                              "price": (order.price - coffee_discount),
                                              "free_coffee_count": free_coffees_count})

    ebh.publish_order_event(
        order={"user_id": order.user_id, "order_id": order.id, "price": (order.price - coffee_discount)})

    return order


@router.put("/employee/order/{order_id}", response_model=Order)
def update_order(order_id: int, status: str = 'delivered', db: SessionLocal = Depends(get_db),
                 ebh: EventBusHandler = Depends(get_ebh)) -> Order:
    order = order_status_update(db, order_id, status)
    # ebh.publish_order_event(order={"user_id": order.user_id, "order_id": order.id, "price": order.price})
    return order
