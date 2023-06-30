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
    limitPrice: float  
    unfilledSize: int  
    status: str        
    filledSize: int
    reduceOnly: bool
    receivedTime: str  = ''
    lastUpdateTime: str = ''
    cliOrdId: str = ''
    
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
        # return f"Order Id: '{self.orderId}', cliOrdId: '{self.cliOrdId}', type: '{self.type}', symbol: '{self.symbol}', side: '{self.side}', quantity: {self.quantity}, filled: {self.filled}, limitPrice: {self.limitPrice}, reduceOnly: {self.reduceOnly}, timestamp: '{self.timestamp}', lastUpdateTimestamp: '{self.lastUpdateTimestamp}'"
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
    order: OrderEvent

    def __str__(self) -> str:
        return f"Success: {self.success}\n{self.order}"