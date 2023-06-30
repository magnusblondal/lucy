import shortuuid

def generate_id():
    return shortuuid.ShortUUID().random(length=10)

class Id:
    id: str = None

    def __init__(self, id: str = None) -> None:
        self.id = id or generate_id()

    def __str__(self) -> str:
        return self.id

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Id):
            return self.id == o.id
        return False

    def make_combined_id(self) -> str:
        return f"{self.id}_{generate_id()}"
    

    @staticmethod
    def make():
        return Id(generate_id())

