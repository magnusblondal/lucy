
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
        sym = f"{self.symbol}"
        typ = f"type: {self.type}"
        underl = f"underlying: {self.underlying}"
        t_size = f"tick_size: {self.tick_size}"
        size = f"contract_size: {self.contract_size}"
        trabl = f"tradeable: {self.tradeable}"
        ims = f"impact_mid_size: {self.impact_mid_size}"
        mps = f"max_position_size: {self.max_position_size}"
        od = f"opening_date: {self.opening_date}"
        fre = f"funding_rate_coefficient: {self.funding_rate_coefficient}"
        mrfr = f"max_relative_funding_rate: {self.max_relative_funding_rate}"
        isin = f"isin: {self.isin}"
        cvtp = f"contr_val_trade_prec: {self.contract_value_trade_precision}"
        po = f"post_only: {self.post_only}"
        fsu = f"fee_schedule_uid: {self.fee_schedule_uid}"
        cat = f"category: {self.category}"
        return f"{sym} {typ} {underl} {t_size} {size} {trabl} {ims} {mps} {od} {fre} {mrfr} {isin} {cvtp} {po} {fsu} {cat}"

    @staticmethod
    def from_kraken(inst) -> 'Instrument':
        i = Instrument()
        i.symbol = val(inst, 'symbol', '')
        # "futures_inverse",
        i.type = val(inst, 'type')
        # "rr_xbtusd",
        i.underlying = val(inst, 'underlying', '')
        i.tick_size = val(inst, 'tickSize')
        i.contract_size = val(inst, 'contractSize')
        i.tradeable = val(inst, 'tradeable')
        i.impact_mid_size = val(inst, 'impactMidSize')
        i.max_position_size = val(inst, 'maxPositionSize')
        i.opening_date = val(inst, 'openingDate')
        i.funding_rate_coefficient = val(
            inst, "fundingRateCoefficient")
        i.max_relative_funding_rate = val(
            inst, "maxRelativeFundingRate")
        i.isin = val(inst, "isin")
        i.contract_value_trade_precision = val(
            inst, "contractValueTradePrecision")
        i.post_only = val(inst, "postOnly")
        i.fee_schedule_uid = val(inst, "feeScheduleUid")
        i.category = val(inst, "category")
        # i.tags = inst["tags"]
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
