from fastapi import APIRouter, status

from ..models.create_bot import CreateDcaBot
from ..models.bot import DcaBot
from ..infrastructure.repos.bot_repository import BotRepository

router = APIRouter()

@router.get("/bot")
def all_bots():
    bots = BotRepository().fetch_bots()
    return {"data": bots}

@router.get("/bot/{bot_id}")
def bot(bot_id: str):
    return {"data": BotRepository().fetch_bot(bot_id)}


@router.get("/bot/{bot_id}/summary")
def bot(bot_id: str):
    bot = BotRepository().fetch_bot(bot_id)
    positionsCnt = len(bot.positions)
    open_positions = bot.num_open_positions()

    resp = { 
        "id": bot.id,
        "name": bot.name,
        "description": bot.description,
        "capital": bot.capital,
        "entry_size": bot.entry_size,
        "so_size": bot.so_size,
        "max_safety_orders": bot.max_safety_orders,
        "allow_shorts": bot.allow_shorts,
        "positions": positionsCnt,
        "currently_open_positions": open_positions,
        "profit": bot.profit() }

    return {"data": resp}

@router.post("/bot", status_code = status.HTTP_201_CREATED)
def create_bot(create_bot: CreateDcaBot):
    bot = DcaBot.create_new(create_bot)
    BotRepository().save(bot)