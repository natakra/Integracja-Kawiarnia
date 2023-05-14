from fastapi import FastAPI

from reservationService.src.router.reservationrouter import router

app = FastAPI()


@app.get('/')
def root():
    return {"message": "Hello World"}


app.include_router(router)
