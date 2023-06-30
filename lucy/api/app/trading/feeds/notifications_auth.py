

class NotificationsAuth:
    notifications = list[str]

    def __init__(self, notifications: list[str]) -> None:
        self.notifications = notifications

    def add(self, notifications: list[str]) -> None:
        self.notifications.extend(notifications)

    def __str__(self) -> str:
        return f"NotificationsAuth:: notifications: {self.notifications}"
    
# {'feed': 'notifications_auth', 'notifications': []}