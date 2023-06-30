
class TrailingStopOptions:
    max_deviation: float
    '''The maximum distance the trigger price may be away from the trigger signal'''
    unit: str	
    '''The unit of the deviation, one of: 'percent' or 'quote_currency' '''

    def __init__(self, max_deviation: float, unit: str) -> None:
        self.max_deviation = max_deviation
        self.unit = unit
    
    @staticmethod
    def from_feed(data = None) -> 'TrailingStopOptions':
        return None if data is None else TrailingStopOptions(
            data['max_deviation'],
            data['unit'])

class OpenOrder:
    instrument: str
    '''The instrument (referred also as symbol or product_id) of the order'''
    time: float
    '''The UTC time in milliseconds'''
    last_update_time: float
    '''The UTC time in milliseconds that the order was last updated'''
    qty: float
    '''The remaining quantity of the order'''
    filled: float
    '''The amount of the order that has been filled'''
    limit_price: float
    '''The limit price of the order'''
    stop_price: float
    '''The stop price of the order'''
    type: float
    '''The order type, 'limit', 'stop', or 'take_profit' '''
    order_id: float
    '''The order id'''
    direction: float
    '''The direction of the order, either 0 for a buy order or 1 for a sell order'''
    reduce_only: float
    '''If true, the order can only reduce open positions, it cannot increase or open new positions'''
    cli_ord_id: str
    '''The unique client order identifier. This field is returned only if the order has a client order id'''
    triggerSignal: str
    '''Trigger signal selected for take profit or stop loss order. Options are 'last', 'mark', or 'spot'. Returned only for take profit or stop loss orders'''
    trailing_stop_options: TrailingStopOptions
    '''If this order is a trailing stop, this contains its parameters'''
    is_cancel: bool
    '''If false the open order has been either placed or partially filled and needs to be updated. If true the open order was either fully filled or cancelled and must be removed from open orders snapshot'''
    reason: str

    def __init__(self, instrument: str, time: float, last_update_time: float, qty: float, filled: float, limit_price: float, 
                 stop_price: float, type: float, order_id: float, direction: float, reduce_only: float, is_cancel: bool, 
                 reason: str, cli_ord_id: str, triggerSignal: str, trailing_stop_options: TrailingStopOptions) -> None:
        self.instrument = instrument
        self.time = time
        self.last_update_time = last_update_time
        self.qty = qty
        self.filled = filled
        self.limit_price = limit_price
        self.stop_price = stop_price
        self.type = type
        self.order_id = order_id
        self.direction = direction
        self.reduce_only = reduce_only
        self.is_cancel = is_cancel
        self.reason = reason
        self.cli_ord_id = cli_ord_id
        self.triggerSignal = triggerSignal
        self.trailing_stop_options = trailing_stop_options
    
    def __str__(self) -> str:
        return f"OpenOrder:: instrument: {self.instrument}, time: {self.time}, last_update_time: {self.last_update_time}, qty: {self.qty}, filled: {self.filled}, limit_price: {self.limit_price}, stop_price: {self.stop_price}, type: {self.type}, order_id: {self.order_id}, direction: {self.direction}, reduce_only: {self.reduce_only}, is_cancel: {self.is_cancel}, reason: {self.reason} cli_ord_id: {self.cli_ord_id}, triggerSignal: {self.triggerSignal}, trailing_stop_options: {self.trailing_stop_options if self.trailing_stop_options is not None else 'None'}."

    @staticmethod
    def from_feed(data) -> 'OpenOrder':
        order = data['order'] if 'order' in data else data
        return OpenOrder(
            order['instrument']              if 'instrument'            in order else None,
            order['time']                    if 'time'                  in order else None,
            order['last_update_time']        if 'last_update_time'      in order else None,
            order['qty']                     if 'qty'                   in order else None,
            order['filled']                  if 'filled'                in order else None,
            order['limit_price']             if 'limit_price'           in order else None,
            order['stop_price']              if 'stop_price'            in order else None,
            order['type']                    if 'type'                  in order else None,
            order['order_id']                if 'order_id'              in order else None,
            order['direction']               if 'direction'             in order else None,
            order['reduce_only']             if 'reduce_only'           in order else False,
            data['is_cancel']                if 'is_cancel'             in data else False,
            data['reason']                   if 'reason'                in data else None,
            order['cli_ord_id']              if 'cli_ord_id'            in order else None,
            order['triggerSignal']           if 'triggerSignal'         in order else None,
            TrailingStopOptions.from_feed(order['trailing_stop_options'])   if 'trailing_stop_options' in order else None,
        )

class OpenOrders:
    orders: list[OpenOrder]
    
    def __init__(self, orders: list[OpenOrder]) -> None:
        self.orders = orders

    def __str__(self) -> str:
        orders = "\n  ".join([str(order) for order in self.orders]) if len(self.orders) > 0 else ""
        orders = f"\n  {orders}" if len(orders) > 0 else "No orders"
        return f"OpenOrders:: orders: {orders}"
    
    def remove(self, order: OpenOrder) -> None:
        self.orders = [o for o in self.orders if o.order_id != order.order_id]
    
    def add(self, order: OpenOrder) -> None:
        self.orders.append(order)

    def update(self, order: OpenOrder) -> None:
        actions = {
            'new_placed_order_by_user': self.new_placed_order_by_user,
            'liquidation': self.liquidation,
            'stop_order_triggered': self.stop_order_triggered,
            'limit_order_from_stop': self.limit_order_from_stop,
            'partial_fill': self.partial_fill,
            'full_fill': self.full_fill,
            'cancelled_by_user': self.cancelled_by_user,
            'contract_expired': self.contract_expired,
            'not_enough_margin': self.not_enough_margin,
            'market_inactive': self.market_inactive,
            'cancelled_by_admin': self.cancelled_by_admin,
            'edited_by_user': self.edited_by_user,
        }
        if order.reason in actions:
            actions[order.reason](order)
        else:
            print(f"OpenOrders.update:: Unknown order reason: {order.reason}")
        if order.is_cancel:
            self.remove(order)

    def new_placed_order_by_user(self, order: OpenOrder):
        '''User placed a new order'''
        self.orders.append(order)

    def edited_by_user(self, order: OpenOrder) -> None:
        '''User edited an order'''
        self.remove(order)
        self.orders.append(order)

    def liquidation(self, order: OpenOrder):
        '''User position liquidated. The order cancelled'''
        self.remove(order)
    
    def stop_order_triggered(self, order: OpenOrder):
        '''A stop order triggered. The system removed the stop order'''
        self.remove(order)
    
    def limit_order_from_stop(self, order: OpenOrder):
        '''The system created a limit order because an existing stop order triggered'''
        self.orders.append(order)
    
    def partial_fill(self, order: OpenOrder):
        '''The order filled partially'''
        # TODO: Implement partial fill
        pass

    def full_fill(self, order: OpenOrder):
        '''The order filled fully and removed'''
        self.remove(order)

    def cancelled_by_user(self, order: OpenOrder):
        '''The order cancelled by the user and removed'''
        self.remove(order)

    def contract_expired(self, order: OpenOrder):
        '''The order contract expired. All open orders of that contract removed'''
        self.add(order)

    def not_enough_margin(self, order: OpenOrder):
        '''The order removed due to insufficient margin'''
        self.remove(order)

    def market_inactive(self, order: OpenOrder):
        '''The order removed because market became inactive'''
        self.remove(order)

    def cancelled_by_admin(self, order: OpenOrder):
        '''The order removed by administrator's action'''
        self.remove(order)
        

    @staticmethod
    def from_feed(data) -> 'OpenOrders':
        '''Snapshot of the user open orders'''
        return OpenOrders(
            [OpenOrder.from_feed(order) for order in data['orders']])


# is_cancel	                boolean	            If false the open order has been either placed or partially filled and needs to be updated. If true the open order was either fully filled or cancelled and must be removed from open orders snapshot			
# reason	                string	            Reason behind the received delta.
#   new_placed_order_by_user:           User placed a new order
#   liquidation:                        User position liquidated. The order cancelled
#   stop_order_triggered:               A stop order triggered. The system removed the stop order
#   limit_order_from_stop:              The system created a limit order because an existing stop order triggered
#   partial_fill:                       The order filled partially
#   full_fill:                          The order filled fully and removed
#   cancelled_by_user:                  The order cancelled by the user and removed
#   contract_expired:                   The order contract expired. All open orders of that contract removed
#   not_enough_margin:                  The order removed due to insufficient margin
#   market_inactive:                    The order removed because market became inactive
#   cancelled_by_admin:                 The order removed by administrator's action			


# account	            string	            '''The user account'''
# orders	            list of structures	'''A list containing the user open orders'''
# instrument	        string	            '''The instrument (referred also as symbol or product_id) of the order'''
# time	                positive integer	'''The UTC time in milliseconds'''
# last_update_time	    positive integer	'''The UTC time in milliseconds that the order was last updated'''
# qty	                positive float	    '''The remaining quantity of the order'''
# filled	            positive float	    '''The amount of the order that has been filled'''
# limit_price	        positive float	    '''The limit price of the order'''
# stop_price	        positive float	    '''The stop price of the order'''
# type	                string	            '''The order type, limit, stop, or take_profit'''
# order_id	            UUID	            '''The order id'''
# cli_ord_id	        UUID	            '''The unique client order identifier. This field is returned only if the order has a client order id'''
# direction	            integer	            '''The direction of the order, either 0 for a buy order or 1 for a sell order'''
# reduce_only	        boolean	            '''If true, the order can only reduce open positions, it cannot increase or open new positions'''
# triggerSignal	        string	            '''Trigger signal selected for take profit or stop loss order. Options are last, mark, or spot. Returned only for take profit or stop loss orders'''
# trailing_stop_options	structure	        '''If this order is a trailing stop, this contains its parameters'''







# 'feed': 'open_orders',
# 'order': {
#     'instrument': 'PF_XBTUSD',
#     'time': 1687800638611,
#     'last_update_time': 1687800638611,
#     'qty': 0.0001,
#     'filled': 0.0,
#     'limit_price': 20666.0,
#     'stop_price': 0.0,
#     'type': 'limit',
#     'order_id': '4436b6db-9d2e-402e-8778-3f583c9dc035',
#     'direction': 0,
#     'reduce_only': False
#     },
# 'is_cancel': False,
# 'reason': 'new_placed_order_by_user'