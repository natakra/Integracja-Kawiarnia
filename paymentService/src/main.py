import traceback
from typing import List

import stripe
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from paymentService.src.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


class Product(BaseModel):
    id: str


class PaymentRequest(BaseModel):
    items: List[Product]


@app.post("/create-payment-intent")
async def root(request: PaymentRequest):
    stripe.api_key = \
        "sk_test_51N7DrUHoWwrUTQHVZgenn8y5DleceuIVDSbTHqwVCurYXbTWC5FV9a9ozb7z6Y67RlTneXduD3W0m7RJk8r42Utn00zfmksxqt"

    data = request

    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data.items),
            currency='pln',
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return {
            'clientSecret': intent['client_secret']
        }
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"{traceback.print_exception(e)}")


@app.on_event("startup")
def on_startup():
    pass


@app.on_event("shutdown")
def on_shutdown():
    pass
