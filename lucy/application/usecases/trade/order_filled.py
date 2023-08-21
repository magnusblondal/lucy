
from lucy.application.trading.feeds.fills import Fill, Fills
from lucy.infrastructure.repos.fills_repository import FillsRepository
from lucy.model.id import Id
from ..usecase import Usecase
import lucy.application.events.bus as bus
from lucy.main_logger import MainLogger

class OrderFilledResult:
    def __init__(self, success: bool, order_ids: list[Id]):
        self.success = success
        self.order_ids = order_ids
    
    def __bool__(self):
        return self.success
    
    def __str__(self):
        return f"OrderFillResult: Success: {self.success}, Order ids: {self.order_ids}"

class OrderFilled(Usecase):
    def __init__(self):
        self.logger =  MainLogger.get_logger(__name__)
        
    def handle(self, fills: Fills) -> OrderFilledResult:
        evs = []
        for fill in fills:
            FillsRepository().add(fill)
            evs = fill.events()
        # print(f"OrderFilled: publishing {len(evs)} : {evs}")
        bus.publish(evs)
        ids = [fill.order_id for fill in fills]
        result =  OrderFilledResult(True, ids)
        self.logger.info(f"OrderFilled: returning {result}")
        return result
    