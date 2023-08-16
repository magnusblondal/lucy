from datetime import datetime
from pydantic import BaseModel
from dataclasses_json import dataclass_json
from dataclasses import dataclass

class Execution(BaseModel):
    uid: str # '45c4bb6f-9ce3-4258-82b1-b27b8f9815ae', 
    timestamp: datetime # 1685130589916, 
    quantity: float # '1', 
    price: float # '10.56000000', 
    markPrice: float # '10.55708715830', 
    limitFilled: bool # False, 
    executionType: str # 'taker', 
    usdValue: float # '10.56', 
    
    positionSize: float # '3'
    fee: float # '0.00528000000'

    orderUid: str    # '57b4e666-ddfa-44bb-810b-caabca9f9bb2', 
    accountUid: str # 'e8d555f5-e7d3-42a5-b9fa-66fcdf856405', 
    tradeable: str  # 'PF_ATOMUSD', 
    direction: str  # 'Buy', 
    orderQuantity: float   # '1', 
    filled: float # '0', 
    orderTimestamp: datetime  # 1685130589916, 
    limitPrice: float # '10.6650000000', 
    orderType: str  # 'IoC', 
    clientId: str   # '', 
    reduceOnly: bool # False, 
    lastUpdateTimestamp: datetime    # 1685130589916

    # orderData: str # {
    #     'positionSize': '3', 
    #     'fee': '0.00528000000'
    

    # 'order': {
    #     'uid': '57b4e666-ddfa-44bb-810b-caabca9f9bb2', 
    #     'accountUid': 'e8d555f5-e7d3-42a5-b9fa-66fcdf856405', 
    #     'tradeable': 'PF_ATOMUSD', 
    #     'direction': 'Buy', 
    #     'quantity': '1', 
    #     'filled': '0', 
    #     'timestamp': 1685130589916, 
    #     'limitPrice': '10.6650000000', 
    #     'orderType': 'IoC', 
    #     'clientId': '', 
    #     'reduceOnly': False, 
    #     'lastUpdateTimestamp': 1685130589916
    # },

    @staticmethod
    def from_kraken(x: dict):
        return Execution(
            uid = x['uid'],
            timestamp = datetime.fromtimestamp(x['timestamp']/1000),
            quantity = float(x['quantity']),
            price = float(x['price']),
            markPrice = float(x['markPrice']),
            limitFilled = x['limitFilled'],
            executionType = x['executionType'],
            usdValue = float(x['usdValue']),

            positionSize = float(x['orderData']['positionSize']),
            fee = float(x['orderData']['fee']),

            orderUid = x['order']['uid'],
            accountUid = x['order']['accountUid'],
            tradeable = x['order']['tradeable'],
            direction = x['order']['direction'],
            orderQuantity = float(x['order']['quantity']),
            filled = float(x['order']['filled']),
            orderTimestamp = datetime.fromtimestamp(x['order']['timestamp']/1000),
            limitPrice = float(x['order']['limitPrice']),
            orderType = x['order']['orderType'],
            clientId = x['order']['clientId'],
            reduceOnly = bool(x['order']['reduceOnly']),
            lastUpdateTimestamp = datetime.fromtimestamp(x['order']['lastUpdateTimestamp']/1000) )