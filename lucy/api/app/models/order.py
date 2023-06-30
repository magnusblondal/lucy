from datetime import datetime

from .id import Id

class Order:
    id: Id
    position_id: Id 
    bot_id: Id
    symbol: str
    qty: float
    price: float
    order_type: str
    side: str
    type: str
    filled: float
    limit_price: float
    reduce_only: bool
    order_created_at: datetime 
    last_update_timestamp: datetime
    exchange_id: str
    created_at: datetime

    def __init__(self, id: Id, position_id: Id , bot_id: Id, symbol: str, qty: float, price: float, order_type: str,
                 side: str, type: str, filled: float, limit_price: float, reduce_only: bool, 
                 order_created_at: datetime , last_update_timestamp: datetime, exchange_id: str,
                 created_at: datetime) -> None:
        self.id = id 
        self.position_id = position_id
        self.bot_id = bot_id
        self.symbol = symbol
        self.qty = qty
        self.price = price
        self.order_type = order_type
        self.side = side
        self.type = type
        self.filled = filled
        self.limit_price = limit_price
        self.reduce_only = reduce_only
        self.order_created_at = order_created_at
        self.last_update_timestamp = last_update_timestamp
        self.exchange_id = exchange_id
        self.created_at = created_at

    def is_close_order(self) -> bool:
        return self.order_type == "close"
    
    def __str__(self) -> str:
        return f"Order:: id: {self.id}, position_id: {self.position_id}, bot_id: {self.bot_id}, symbol: {self.symbol}, qty: {self.qty}, price: {self.price}, side: {self.side}, type: {self.type}, filled: {self.filled}, limit_price: {self.limit_price}, reduce_only: {self.reduce_only}, order_created_at: {self.order_created_at}, last_update_timestamp: {self.last_update_timestamp}, cli_ord_id: {self.cli_ord_id}, created_at: {self.created_at}"