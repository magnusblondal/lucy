from .event import DomainEvent


class OrderCreatedEvent(DomainEvent):
    def __init__(self, order: 'Order') -> None:
        from lucy.model.order import Order

        super().__init__()
        self.order = order

    def __str__(self) -> str:
        return f"OrderCreatedEvent:: {self.order}"


class OrderFilledEvent(DomainEvent):
    def __init__(
        self,
        fill_id: str,
        order_id: str,
        is_order_filled: bool
    ) -> None:
        super().__init__()
        self.fill_id = fill_id
        self.order_id = order_id
        self.is_order_filled = is_order_filled

    def __str__(self) -> str:
        id = f"Id: {self.fill_id}"
        order = f"Order: {self.order_id}"
        filled = f"Filled: {self.is_order_filled}"
        return f"OrderFilledEvent:: {id} {order} {filled}"
