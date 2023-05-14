import json
import traceback

import requests
from fastapi import APIRouter, HTTPException
from firebase_admin import auth
from pydantic import BaseModel

router = APIRouter()


class AuthInfo(BaseModel):
    email: str
    password: str


@router.post('/login')
def login(auth_info: AuthInfo):
    return login_user(auth_info.email, auth_info.password)


def login_user(username: str, password: str):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key" \
          "=AIzaSyCzeT0NVcjNpTuFo79BwY-Qzv5gqWc6Bi4"
    payload = json.dumps({
        "email": username,
        "password": password,
        "returnSecureToken": True
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


@router.post('/register')
def register(auth_info: AuthInfo):
    try:
        user = auth.create_user(
            email=auth_info.email,
            password=auth_info.password)
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{traceback.print_exception(e)}")


@router.post('/cookies')
def set_cookies():
    pass
