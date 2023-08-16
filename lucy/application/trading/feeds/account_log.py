from datetime import datetime

class AccountLog:
    id: int
    '''The identifier of the log'''
    date: datetime
    '''The creation time of the log according to server date and time (ISO8601 datetime)'''
    asset: str
    '''The asset related of the booking'''
    contract: str
    '''The instrument related to the booking ('pf_ethusd').'''
    info: str
    '''A description of the booking'''
    booking_uid: str
    '''The unique id of the booking'''
    margin_account: str
    '''The account name'''
    old_balance: float
    '''The account balance before the described in info action'''
    new_balance: float
    '''The portfolio value calculated as balance plus unrealized pnl value'''
    old_average_entry_price: float
    '''The average entry price of the position prior to this trade'''
    new_average_entry_price: float
    '''The average entry price of the position after this trade'''
    trade_price: float
    '''The price the trade was executed at'''
    mark_price: float
    '''The mark price at the time the trade was executed'''
    realized_pnl: float
    '''The pnl that is realized by reducing the position'''
    fee: float
    '''The fee paid'''
    execution: str
    '''The uid of the associated execution'''
    collateral: str
    '''The currency of the associated entry'''
    funding_rate: float
    '''The absolute funding rate'''
    realized_funding: float
    '''The funding rate realized due to change in position size or end of funding rate period'''
    conversion_spread_percentage: float
    '''The percentage conversion spread used in a currency conversion'''
    liquidation_fee: float
    '''The fee paid for liquidation'''

    def __init__(self, id: int, date: datetime, asset: str, contract: str, info: str,
                booking_uid: str, margin_account: str, old_balance: float, new_balance: float, 
                old_average_entry_price: float,
                new_average_entry_price: float,
                trade_price: float,
                mark_price: float,
                realized_pnl: float,
                fee: float,
                execution: str,
                collateral: str,
                funding_rate: float,
                realized_funding: float,
                conversion_spread_percentage: float,
                liquidation_fee: float
    ):
        self.id = id
        self.date = date
        self.asset = asset
        self.contract = contract
        self.info = info
        self.booking_uid = booking_uid
        self.margin_account = margin_account
        self.old_balance = old_balance
        self.new_balance = new_balance
        self.old_average_entry_price = old_average_entry_price
        self.new_average_entry_price = new_average_entry_price
        self.trade_price = trade_price
        self.mark_price = mark_price
        self.realized_pnl = realized_pnl
        self.fee = fee
        self.execution = execution
        self.collateral = collateral
        self.funding_rate = funding_rate
        self.realized_funding = realized_funding
        self.conversion_spread_percentage = conversion_spread_percentage
        self.liquidation_fee = liquidation_fee

    def __str__(self):
        return f"AccountLog:: id={self.id} info: '{self.info}' asset: {self.asset}  contract: {self.contract}, margin_account={self.margin_account}, old_balance={self.old_balance}, new_balance={self.new_balance}, old_average_entry_price={self.old_average_entry_price}, new_average_entry_price={self.new_average_entry_price}, trade_price={self.trade_price}, mark_price={self.mark_price}, realized_pnl={self.realized_pnl}, fee={self.fee}, execution={self.execution}, collateral={self.collateral}, funding_rate={self.funding_rate}, realized_funding={self.realized_funding}, conversion_spread_percentage={self.conversion_spread_percentage}, liquidation_fee={self.liquidation_fee}, date={self.date}, booking_uid={self.booking_uid}"

    @staticmethod
    def from_feed(data: dict) -> 'AccountLog':
        return AccountLog(
            data['id']                              if 'id' in data else None,
            data['date']                            if 'date' in data else None,
            data['asset']                           if 'asset' in data else None,
            data['contract']                        if 'contract' in data else None,
            data['info']                            if 'info' in data else None,
            data['booking_uid']                     if 'booking_uid' in data else None,
            data['margin_account']                  if 'margin_account' in data else None,
            data['old_balance']                     if 'old_balance' in data else None,
            data['new_balance']                     if 'new_balance' in data else None,
            data['old_average_entry_price']         if 'old_average_entry_price' in data else None,
            data['new_average_entry_price']         if 'new_average_entry_price' in data else None,
            data['trade_price']                     if 'trade_price' in data else None,
            data['mark_price']                      if 'mark_price' in data else None,
            data['realized_pnl']                    if 'realized_pnl' in data else None,
            data['fee']                             if 'fee' in data else None,
            data['execution']                       if 'execution' in data else None,
            data['collateral']                      if 'collateral' in data else None,
            data['funding_rate']                    if 'funding_rate' in data else None,
            data['realized_funding']                if 'realized_funding' in data else None,
            data['conversion_spread_percentage']    if 'conversion_spread_percentage' in data else None,
            data['liquidation_fee']                 if 'liquidation_fee' in data else None,
        )

class AccountLogs:
    logs: list[AccountLog]

    def __init__(self, logs: list[AccountLog]):
        self.logs = logs
    
    def __str__(self) -> str:
        return f'AccountLogs:: count: {len(self.logs)}'

    def add(self, log: AccountLog) -> None:
        self.logs.append(log)
    
    def last(self) -> AccountLog:
        return sorted(self.logs, key=lambda x: x.id, reverse=False)[-1]
    
    def tail(self, cnt: int = 5) -> list[AccountLog]:
        return sorted(self.logs, key=lambda x: x.id, reverse=False)[-cnt:]
    
    @staticmethod
    def from_feed(data: dict) -> 'AccountLogs':
        return AccountLogs([AccountLog.from_feed(log) for log in data['logs']])
