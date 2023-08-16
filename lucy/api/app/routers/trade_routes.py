from fastapi import APIRouter, status

from lucy.application.usecases.trade.sell import Sell
from lucy.application.usecases.trade.buy import Buy

router = APIRouter()

@router.get("/trade/{symbol}/sell/{qty}")
def sell(symbol: str, qty: float):
    order = Sell().handle(symbol, qty)
    return {"data": order}

@router.get("/trade/{symbol}/buy/{qty}")
def sell(symbol: str, qty: float):
    order = Buy().handle(symbol, qty)
    return {"data": order}
