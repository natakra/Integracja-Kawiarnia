import traceback

import firebase_admin
from fastapi import Depends
from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from fastapi_gateway import route
from firebase_admin import auth, credentials
from pydantic import BaseModel
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response

from reservationService.src.schemas.reservation_schemas import CreateReservation

app = FastAPI(title='API Gateway')
SERVICE_URL = "http://localhost:8000"

API_KEY_NAME = "x-api-key"

api_key_header = APIKeyHeader(
    name=API_KEY_NAME,
    auto_error=False
)


@app.on_event("startup")
def startup():
    cred = credentials.Certificate("userService/src/firebase_config.json")
    firebase_admin.initialize_app(cred)


def verify_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token['uid']
    except Exception as e:
        print(traceback.print_exception(e))
        return None


def check_api_key(key: str = Depends(api_key_header)):
    print(verify_token(key))

    if verify_token(key):
        return key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You didn't pass the api key in the header! Header: x-api-key",
    )


class FooModel(BaseModel):
    example_int: int
    example_str: str


@route(
    request_method=app.get,
    service_url=SERVICE_URL,
    gateway_path='/tables/{path}',
    service_path='/tables/{path}',
    status_code=status.HTTP_200_OK,
    tags=['Query', 'Body', 'Path'],
    dependencies=[
        Depends(check_api_key)
    ],
)
async def check_query_params_and_body(
        path: int, request: Request, response: Response
):
    pass


@route(
    request_method=app.post,
    service_url=SERVICE_URL,
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
