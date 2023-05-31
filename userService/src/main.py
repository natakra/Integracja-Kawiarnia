import firebase_admin
from fastapi import FastAPI
from firebase_admin import credentials

from src.router.userrouter import router

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
def startup():
    cred = credentials.Certificate("src/firebase_config.json")
    firebase_admin.initialize_app(cred)
