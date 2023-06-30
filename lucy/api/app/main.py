from fastapi import FastAPI
from .routers import bot_routes, trade_routes, tv_signal_routes

app = FastAPI()

app.include_router(bot_routes.router)
app.include_router(tv_signal_routes.router)
app.include_router(trade_routes.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}