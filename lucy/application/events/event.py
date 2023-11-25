
class Event:
    def __str__(self) -> str:
        return ""


class DomainEvent(Event):
    def __str__(self) -> str:
        return super().__str__() + "DomainEvent:: "
