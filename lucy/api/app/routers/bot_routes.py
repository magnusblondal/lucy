from fastapi import APIRouter, status

from lucy.api.logging_api import ApiLogger

from lucy.model.create_bot import CreateDcaBot
from lucy.model.bot import DcaBot
from lucy.infrastructure.repos.bot_repository import BotRepository

router = APIRouter()
logger = ApiLogger.get_logger("bot_routes")

@router.get("/bots")
def all_bots():
    logger.info("Fetching all bots")
    bots = BotRepository().fetch_bots()
    return {"data": bots}

@router.get("/bots/{bot_id}")
def bot(bot_id: str):
    return {"data": BotRepository().fetch(bot_id)}


@router.get("/bots/{bot_id}/summary")
def bot(bot_id: str):
    bot = BotRepository().fetch(bot_id)
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

@router.post("/bots", status_code = status.HTTP_201_CREATED)
def create_bot(create_bot: CreateDcaBot):
    bot = DcaBot.create_new(create_bot)
    BotRepository().add(bot)