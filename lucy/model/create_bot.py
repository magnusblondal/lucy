

from typing import Optional
from pydantic import BaseModel
from lucy.model.interval import Interval

class CreateBot(BaseModel):
    pass

class CreateDcaBot(CreateBot):
    name: str
    description: Optional[str]
    capital: float
    entry_size: float
    so_size: float
    max_safety_orders: int
    allow_shorts: bool
    max_positions_allowed: int
    interval: int
    symbol: str
    active: bool = True
    strategy: str = 'BBbreakout'

class EditDcaBot(CreateDcaBot):
    pass

