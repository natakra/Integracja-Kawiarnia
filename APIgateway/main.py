import json
import os
import traceback
from enum import Enum
from typing import List

import firebase_admin
from fastapi import Depends
from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from fastapi_gateway import route
from firebase_admin import auth, credentials
from firebase_admin.auth import ExpiredIdTokenError
from pydantic import BaseModel
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response


class BaseReservation(BaseModel):
    table_id: int
    reservation_time: str

    class Config:
        orm_mode = True


class CreateReservation(BaseReservation):
    pass


class OrderStatus(Enum):
    STATUS_ACCEPTED = "accepted"
    STATUS_PAID = "paid"
    STATUS_CANCELLED = "cancelled"
    STATUS_DONE = "done"


class CreateOrder(BaseModel):
    product_ids: List[int]

    class Config:
        orm_mode = True


class Order(BaseModel):
    user_id: str
    id: int
    price: float
    status: OrderStatus

    class Config:
        orm_mode = True


app = FastAPI(title='API Gateway')
RESERVATION_SERVICE_URL = os.getenv("RESERVATION_SERVICE_URL")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL")
MENU_SERVICE_URL = os.getenv("MENU_SERVICE_URL")
LOYALTY_SERVICE_URL = os.getenv("LOYALTY_SERVICE_URL")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL")

API_KEY_NAME = "x-api-key"

api_key_header = APIKeyHeader(
    name=API_KEY_NAME,
    auto_error=False
)


@app.on_event("startup")
def startup():
    cred = credentials.Certificate("./firebase_config.json")
    firebase_admin.initialize_app(cred)


def verify_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token['uid']
    except ValueError as e:
        print(traceback.print_exception(e))
        return None


def check_api_key(key: str = Depends(api_key_header)):
    try:
        uid = verify_token(key)
    except ExpiredIdTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired!",
        )
    if uid is not None:
        return uid
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You didn't pass the api key in the header! Header: x-api-key",
    )


async def get_body_as_string(request: Request):
    return json.loads(await request.body())


class FooModel(BaseModel):
    example_int: int
    example_str: str


@route(
    request_method=app.get,
    service_url=RESERVATION_SERVICE_URL,
    gateway_path='/tables/availability',
    service_path='/tables/availability',
    query_params=["time"],
    status_code=status.HTTP_200_OK,
    tags=['Query'],
    dependencies=[
        Depends(check_api_key)
    ],
)
async def check_tables_availability(
        time: str, request: Request, response: Response
):
    pass


@route(
    request_method=app.get,
    service_url=RESERVATION_SERVICE_URL,
    gateway_path='/tables/{path}',
    service_path='/tables/{path}',
    status_code=status.HTTP_200_OK,
    tags=['Query', 'Body', 'Path'],
    dependencies=[
        Depends(check_api_key)
    ],
)
async def check_table_by_id(
        path: int, request: Request, response: Response
):
    pass


class AuthInfo(BaseModel):
    email: str
    password: str


@route(
    request_method=app.post,
    service_url=USER_SERVICE_URL,
    gateway_path='/login',
    service_path='/login',
    status_code=status.HTTP_200_OK,
    tags=['Query', 'Body', 'Path'],
    body_params=["body"]
)
async def login(
        body: AuthInfo, request: Request, response: Response
):
    pass


@route(
    request_method=app.post,
    service_url=USER_SERVICE_URL,
    gateway_path='/register',
    service_path='/register',
    status_code=status.HTTP_200_OK,
    tags=['Query', 'Body', 'Path'],
    body_params=["body"]
)
async def register(
        body: AuthInfo, request: Request, response: Response
):
    pass


@route(
    request_method=app.post,
    service_url=RESERVATION_SERVICE_URL,
    gateway_path='/reservation',
    service_path='/reservation',
    status_code=status.HTTP_200_OK,
    body_params=["reservation_form"],
    query_params=["user_id"],
    tags=['Query', 'Body', 'Path'],
)
async def post_reservation(
        reservation_form: CreateReservation, request: Request, response: Response, user_id: str = Depends(check_api_key)
):
    pass


@route(
    request_method=app.delete,
    service_url=RESERVATION_SERVICE_URL,
    gateway_path='/reservation/{path}',
    service_path='/reservation/{path}',
    status_code=status.HTTP_202_ACCEPTED,
    tags=['Query', 'Body', 'Path'],
    dependencies=[
        Depends(check_api_key)
    ],
)
async def delete_reservation(
        path: int, request: Request, response: Response
):
    pass


@route(
    request_method=app.post,
    service_url=ORDER_SERVICE_URL,
    gateway_path='/order',
    service_path='/order',
    status_code=status.HTTP_200_OK,
    tags=['Query', 'Body', 'Path'],
    body_params=["order_form"],
    query_params=["user_id"],
    dependencies=[
        Depends(check_api_key)
    ],
)
async def create_order(
        order_form: CreateOrder, request: Request, response: Response, user_id: str = Depends(check_api_key)
):
    pass


@route(
    request_method=app.post,
    service_url=PAYMENT_SERVICE_URL,
    gateway_path='/create-payment-intent/{order_id}',
    service_path='/create-payment-intent/{order_id}',
    status_code=status.HTTP_200_OK,
    tags=['Query', 'Body', 'Path'],
)
async def payment_intent(
        order_id: int, request: Request, response: Response
):
    pass


@route(
    request_method=app.post,
    service_url=PAYMENT_SERVICE_URL,
    gateway_path='/stripe_webhooks',
    service_path='/stripe_webhooks',
    status_code=status.HTTP_200_OK,
    body_params=["body"],
    tags=['Query', 'Body', 'Path'],
)
async def payment_webhook(
        request: Request, response: Response, body: dict = Depends(get_body_as_string)
):
    pass


@route(
    request_method=app.get,
    service_url=MENU_SERVICE_URL,
    gateway_path='/menu',
    service_path='/menu',
    status_code=status.HTTP_200_OK,
    tags=['Query', 'Body', 'Path'],
    dependencies=[
        Depends(check_api_key)
    ]
)
async def get_menu(
        request: Request, response: Response
):
    pass


@route(
    request_method=app.get,
    service_url=MENU_SERVICE_URL,
    gateway_path='/menu',
    service_path='/menu',
    status_code=status.HTTP_200_OK,
    tags=['Query', 'Body', 'Path'],
    dependencies=[
        Depends(check_api_key)
    ]
)
async def get_menu(
        request: Request, response: Response
):
    pass


@route(
    request_method=app.get,
    service_url=LOYALTY_SERVICE_URL,
    gateway_path='/loyalty/points',
    service_path='/loyalty/points',
    status_code=status.HTTP_200_OK,
    tags=['Query', 'Body', 'Path'],
    query_params=['user_id'],
    dependencies=[
        Depends(check_api_key)
    ]
)
async def get_loyalty_points(
        request: Request, response: Response, user_id: str = Depends(check_api_key)
):
    pass
