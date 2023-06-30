
from datetime import datetime


class Heartbeat:
    time: int

    def __init__(self, time: int) -> None:
        self.time = time

    def __str__(self) -> str:
        return f"Heartbeat:: time: {self.time} -- {self.date_time()}"
    
    def date_time(self) -> datetime:
        return datetime.fromtimestamp(self.time/1000)
    
    @staticmethod
    def from_feed(data) -> 'Heartbeat':
        print(data)
        return Heartbeat(data['time'])