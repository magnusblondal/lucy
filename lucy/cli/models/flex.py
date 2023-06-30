from decimal import Decimal


def rnd(d: float, precision: int = 2):
    if d is None:
        return 0
    return d if d == 0 else round(d, precision)

class Currency:
    currency: str
    quantity: float
    value: float
        
    def __init__(self, curr: str, data) -> None:
        self.currency = curr
        self.quantity = float(data['quantity'])
        self.value = float(data['value'])

    def __str__(self) -> str:
        prec = 2 if self.currency == 'USD' else 6
        return f"{self.currency}\n" +\
            f"   quantity: {rnd(self.quantity, prec)}\n" +\
            f"   value: {rnd(self.value)}\n"

class FuturesCurrency(Currency):
    collateral: float
    available: float

    def __init__(self, curr: str, data) -> None:
        super().__init__(curr, data)
        self.collateral = float(data['collateral'])
        self.available = float(data['available'])
    
    
    def __str__(self) -> str:
        return f"{super().__str__()}" +\
            f"   collateral: {rnd(self.collateral)}\n" +\
            f"   available: {rnd(self.available)}\n"


class Account:
    pass

class Flex(Account):
    initialMargin: float
    initialMarginWithOrders: float
    maintenanceMargin: float
    balanceValue: float
    portfolioValue: float
    collateralValue: float
    pnl: float
    unrealizedFunding: float
    totalUnrealized: float
    totalUnrealizedAsMargin: float
    availableMargin: float
    marginEquity: float
    type: str
    currencies: list[FuturesCurrency]

    def __init__(self, data) -> None:
        self.initialMargin = float(data["initialMargin"])
        self.initialMarginWithOrders = float(data["initialMarginWithOrders"])
        self.maintenanceMargin = float(data["maintenanceMargin"])
        self.balanceValue = float(data["balanceValue"])
        self.portfolioValue = float(data["portfolioValue"])
        self.collateralValue = float(data["collateralValue"])
        self.pnl = float(data["pnl"])
        self.unrealizedFunding = float(data["unrealizedFunding"])
        self.totalUnrealized = float(data["totalUnrealized"])
        self.totalUnrealizedAsMargin = float(data["totalUnrealizedAsMargin"])
        self.availableMargin = float(data["availableMargin"])
        self.marginEquity = float(data["marginEquity"])
        self.type = data["type"]
        self.currencies = [FuturesCurrency(c, data['currencies'][c]) for c in data['currencies']]

    def __str__(self) -> str:
        currs = [f"{s}" for s in self.currencies]
        return ''.join(currs) +\
            f'initialMargin: {rnd(self.initialMargin)}\n' +\
            f'balanceValue: {rnd(self.balanceValue)}\n' +\
            f'initialMargin: {rnd(self.initialMargin)}\n' +\
            f'initialMarginWithOrders: {rnd(self.initialMarginWithOrders)}\n' +\
            f'maintenanceMargin: {rnd(self.maintenanceMargin)}\n' +\
            f'balanceValue: {rnd(self.balanceValue)}\n' +\
            f'portfolioValue: {rnd(self.portfolioValue)}\n' +\
            f'collateralValue: {rnd(self.collateralValue)}\n' +\
            f'pnl: {rnd(self.pnl)}\n' +\
            f'unrealizedFunding: {rnd(self.unrealizedFunding)}\n' +\
            f'totalUnrealized: {rnd(self.totalUnrealized)}\n' +\
            f'totalUnrealizedAsMargin: {rnd(self.totalUnrealizedAsMargin)}\n' +\
            f'availableMargin: {rnd(self.availableMargin)}\n' +\
            f'marginEquity: {rnd(self.marginEquity)}\n' +\
            f'type: {self.type}'
        
