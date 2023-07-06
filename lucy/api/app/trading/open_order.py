from dataclasses_json import dataclass_json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass_json
@dataclass
class OpenOrder:
    order_id: str      
    symbol: str        
    side: str          
    orderType: str     
    limitPrice: float = 0.0
    unfilledSize: int = 0
    status: str = ''        
    filledSize: int = 0
    reduceOnly: bool = False
    receivedTime: str  = ''
    lastUpdateTime: str = ''
    cliOrdId: str = ''
    stopPrice: float = 0.0
    triggerSignal: str = ''
    
@dataclass_json
@dataclass
class OrderEvent:
    orderId: str            
    type: str               
    symbol: str             
    side: str               
    quantity: int           
    filled: int             
    limitPrice: float       
    reduceOnly: bool        
    timestamp: str          
    lastUpdateTimestamp: str
    cliOrdId: Optional[str] = None

    def __str__(self) -> str:
        return f"symbol: '{self.symbol}'\n" +\
            f"Order Id: '{self.orderId}'\n" +\
            f"cliOrdId: '{self.cliOrdId}'\n" +\
            f"type: '{self.type}'\n" +\
            f"side: '{self.side}'\n" +\
            f"quantity: {self.quantity}\n" +\
            f"filled: {self.filled}\n" +\
            f"limitPrice: {self.limitPrice}\n" +\
            f"reduceOnly: {self.reduceOnly}\n" +\
            f"timestamp: '{self.timestamp}'\n" +\
            f"lastUpdateTimestamp: '{self.lastUpdateTimestamp}'"
        
@dataclass
class OrderResults:
    success: bool
    order_event: OrderEvent

    def __str__(self) -> str:
        return f"Success: {self.success}\n{self.order_event}"

{
    'result': 'success', 
    'openOrders': [
        {
            'order_id': '95d5681c-41df-4cfd-b745-cb5c3a8d3780', 
            'symbol': 'pf_dotusd', 
            'side': 'buy', 
            'orderType': 'take_profit', 
            'stopPrice': 4.842, 
            'unfilledSize': 17, 
            'receivedTime': '2023-07-01T03:11:43.000Z', 
            'status': 'untouched', 
            'filledSize': 0, 
            'reduceOnly': True, 
            'triggerSignal': 'mark', 
            'lastUpdateTime': '2023-07-01T03:11:42.945Z'}], 
            'serverTime': '2023-07-04T12:36:59.219Z'
}