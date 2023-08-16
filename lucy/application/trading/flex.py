from decimal import Decimal


def rnd(d: float, precision: int = 2):
    if d is None:
        return 0
    return d if d == 0 else round(d, precision)

def by_keys(data, keys, default=None):
    for k in keys:
        if k in data:
            return data[k]
    return default

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
    conversion_spread: float
    haircut: float

    def __init__(self, curr: str, data) -> None:
        super().__init__(curr, data)
        self.collateral = by_keys(data, ['collateral', 'collateral_value'])
        self.available =  by_keys(data, ['available'])
        self.conversion_spread = by_keys(data, ['conversion_spread'])
        self.haircut = by_keys(data, ['haircut'])
    
    
    def __str__(self) -> str:
        prec = 2 if self.currency == 'USD' else 6
        return f"{self.currency}\tquantity: {rnd(self.quantity, prec)} value: {rnd(self.value)} collateral: {rnd(self.collateral)} available: {rnd(self.available)} conversion_spread: {rnd(self.conversion_spread)} haircut: {rnd(self.haircut)}"
    
    # def __str__(self) -> str:
    #     return f"{super().__str__()}" +\
    #         f"   collateral: {rnd(self.collateral)}\n" +\
    #         f"   available: {rnd(self.available)}\n" +\
    #         f"   conversion_spread: {rnd(self.conversion_spread)}\n" +\
    #         f"   haircut: {rnd(self.haircut)}\n"

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
        self.initialMargin = by_keys(data, ["initialMargin", "initial_margin"])
        self.initialMarginWithOrders = by_keys(data, ["initialMarginWithOrders"])
        self.maintenanceMargin = by_keys(data, ["maintenanceMargin"])
        self.balanceValue = by_keys(data, ["balanceValue"])
        self.portfolioValue = by_keys(data, ["portfolioValue"])
        self.collateralValue = by_keys(data, ["collateralValue"])
        self.pnl = by_keys(data, ["pnl"])
        self.unrealizedFunding = by_keys(data, ["unrealizedFunding"])
        self.totalUnrealized = by_keys(data, ["totalUnrealized"])
        self.totalUnrealizedAsMargin = by_keys(data, ["totalUnrealizedAsMargin"])
        self.availableMargin = by_keys(data, ["availableMargin"])
        self.marginEquity = by_keys(data, ["marginEquity"])
        self.type = by_keys(data, ["type"])
        self.currencies = [FuturesCurrency(c, data['currencies'][c]) for c in data['currencies']]

    def __str__(self) -> str:
        currs = [f"  {s}\n" for s in self.currencies] if self.currencies is not None else []
        return ''.join(currs) +\
            f'  initialMargin: {rnd(self.initialMargin)}\n' +\
            f'  balanceValue: {rnd(self.balanceValue)}\n' +\
            f'  initialMarginWithOrders: {rnd(self.initialMarginWithOrders)}\n' +\
            f'  maintenanceMargin: {rnd(self.maintenanceMargin)}\n' +\
            f'  balanceValue: {rnd(self.balanceValue)}\n' +\
            f'  portfolioValue: {rnd(self.portfolioValue)}\n' +\
            f'  collateralValue: {rnd(self.collateralValue)}\n' +\
            f'  pnl: {rnd(self.pnl)}\n' +\
            f'  unrealizedFunding: {rnd(self.unrealizedFunding)}\n' +\
            f'  totalUnrealized: {rnd(self.totalUnrealized)}\n' +\
            f'  totalUnrealizedAsMargin: {rnd(self.totalUnrealizedAsMargin)}\n' +\
            f'  availableMargin: {rnd(self.availableMargin)}\n' +\
            f'  marginEquity: {rnd(self.marginEquity)}\n' +\
            f'  type: {self.type}'
