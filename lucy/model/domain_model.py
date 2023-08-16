
from lucy.model.id import Id
from lucy.application.events.event import DomainEvent

class DomainModel:
    id: Id
    _events: list[DomainEvent]

    def __init__(self, id: Id) -> None:
        self.id = id if id is not None else Id()
        self._events = []

    def _this_just_happened(self, event: DomainEvent) -> None:
        if self._events is None:
            self._events = []
        self._events.append(event)