import json
import traceback

import stripe
from fastapi import FastAPI, HTTPException, Path, Depends

from src import stripe_event_handler
from src.crud.payment_crud import get_order_by_id
from src.db.database import Base, engine, get_db, SessionLocal
from src.event_bus_handler import EventBusHandler

Base.metadata.create_all(bind=engine)

app = FastAPI()

ebh: EventBusHandler | None = None


def get_ebh():
    return ebh


@app.get("/")
def root():
    return "Running"


@app.post("/create-payment-intent/{order_id}")
async def root(order_id: int = Path(), db: SessionLocal = Depends(get_db)):
    stripe.api_key = \
        "sk_test_51N7DrUHoWwrUTQHVZgenn8y5DleceuIVDSbTHqwVCurYXbTWC5FV9a9ozb7z6Y67RlTneXduD3W0m7RJk8r42Utn00zfmksxqt"

    order = get_order_by_id(order_id, db)

    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(order.price * 100),
            currency='pln',
            automatic_payment_methods={
                'enabled': True,
            },
            metadata={
                "order_id": order_id
            }
        )
        return {
            'clientSecret': intent['client_secret']
        }
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"{traceback.print_exception(e)}")


@app.post("/stripe_webhooks", status_code=200)
async def handle_event(body: dict, db: SessionLocal = Depends(get_db), ebh: EventBusHandler = Depends(get_ebh)):
    def get_order_id(event):
        return event["data"]["object"]["metadata"]["order_id"]

    print()
    # event = await request.json()
    event = body
    order = get_order_by_id(get_order_id(event), db)
    print(event)
    print(event['type'])
    match event['type']:
        case 'payment_intent.succeeded':
            stripe_event_handler.handle_payment_success(order, ebh)
        case 'payment_intent.canceled':
            stripe_event_handler.handle_payment_failed(order, ebh)
        case 'payment_intent.payment_failed':
            stripe_event_handler.handle_payment_failed(order, ebh)


@app.on_event("startup")
async def on_startup():
    global ebh
    ebh = EventBusHandler()
    await ebh.on_startup()


@app.on_event("shutdown")
def on_shutdown():
    ebh.on_shutdown()
