
def val(obj, key, default=None):
    return obj[key] if key in obj.keys() else default

class Instrument:
    symbol: str
    type: str
    underlying: str
    tick_size: float
    contract_size: int
    tradeable: bool
    impact_mid_size: float
    max_position_size: float
    opening_date: str
    funding_rate_coefficient: int
    max_relative_funding_rate: float
    isin: str
    contract_value_trade_precision: int
    post_only: bool
    fee_schedule_uid: str
    category: str
    # tags: 

    def __str__(self) -> str:
        return f"{self.symbol} type: {self.type} underlying: {self.underlying} tick_size: {self.tick_size} contract_size: {self.contract_size} tradeable: {self.tradeable} impact_mid_size: {self.impact_mid_size} max_position_size: {self.max_position_size} opening_date: {self.opening_date} funding_rate_coefficient: {self.funding_rate_coefficient} max_relative_funding_rate: {self.max_relative_funding_rate} isin: {self.isin} contract_value_trade_precision: {self.contract_value_trade_precision} post_only: {self.post_only} fee_schedule_uid: {self.fee_schedule_uid} category: {self.category}"

    @staticmethod
    def from_kraken(inst) -> 'Instrument':
        i =  Instrument()
        i.symbol                            = val(inst, 'symbol', '')                       # "pi_xbtusd",
        i.type                              = val(inst, 'type')                             # "futures_inverse",
        i.underlying                        = val(inst, 'underlying', '')                   # "rr_xbtusd",
        i.tick_size                         = val(inst, 'tickSize')                         # 0.5,
        i.contract_size                     = val(inst, 'contractSize')                     # 1,
        i.tradeable                         = val(inst, 'tradeable')                        # true,
        i.impact_mid_size                   = val(inst, 'impactMidSize')                    # 1000.00,
        i.max_position_size                 = val(inst, 'maxPositionSize')                  # 75000000.00000000000,
        i.opening_date                      = val(inst, 'openingDate')                      # "2018-08-31T00:00:00.000Z",
        i.funding_rate_coefficient          = val(inst, "fundingRateCoefficient")           # 24,
        i.max_relative_funding_rate         = val(inst, "maxRelativeFundingRate")           # 0.0025,
        i.isin                              = val(inst, "isin")                             # "GB00J62YGL67",
        i.contract_value_trade_precision    = val(inst, "contractValueTradePrecision")      # 0,
        i.post_only                         = val(inst, "postOnly")                         # false,
        i.fee_schedule_uid                  = val(inst, "feeScheduleUid")                   # "eef90775-995b-4596-9257-0917f6134766",
        i.category                          = val(inst, "category")                         # "",
        # i.tags = inst["tags"]                                                             # []
        # marginLevels = inst['marginLevels']
        # "retailMarginLevels": [
        return i


class Instruments:
    instruments: dict[Instrument]

    def __init__(self, instruments: list[Instrument]) -> None:
        xs = [(i.symbol, i) for i in instruments]
        self.instruments = dict(xs)

    def __getitem__(self, key: str) -> Instrument:
        return self.instruments[key]

    def __iter__(self):
        return iter(self.instruments.values())
    
    def __len__(self):
        return len(self.instruments)
    
    def pf(self, symbol: str):
        '''Returns the perpetual future symbol for the given symbol'''
        s = f'pf_{symbol.lower()}usd'
        return s if s in self.instruments.keys() else None
    
# rr Reference Rate
# in Real-Time Index
# fi Futures Margin Account

# pf Perpetual Futures
# pi Perpetual Inverse


# Example Symbols	Description
# xbt	Bitcoin
# xrp	Ripple XRP
# fi_xbtusd	Bitcoin-Dollar Futures Margin Account
# fi_xrpusd	Ripple-Dollar Futures Margin Account
# fi_xbtusd_180615	Bitcoin-Dollar Futures, maturing at 16:00 London time on 15 June 2018
# fi_xrpusd_180615	Ripple-Dollar Futures, maturing at 16:00 London time on 15 June 2018
# fi_xrpxbt_180615	Ripple-Bitcoin Futures, maturing at 16:00 London time on 15 June 2018
# in_xbtusd	Bitcoin-Dollar Real-Time Index
# rr_xbtusd	Bitcoin-Dollar Reference Rate
# in_xrpusd	Ripple-Dollar Real-Time Index
