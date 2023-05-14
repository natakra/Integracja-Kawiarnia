import firebase_admin
from fastapi import FastAPI
from firebase_admin import credentials

from userService.src.router.userrouter import router

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
def startup():
    cred = credentials.Certificate("userService/src/firebase_config.json")
    firebase_admin.initialize_app(cred)
