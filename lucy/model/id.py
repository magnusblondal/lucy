import shortuuid

def generate_id():
    return shortuuid.ShortUUID().random(length=10)

class Id:
    id: str

    def __init__(self, id: str = "") -> None:
        self.id = id or generate_id()

    def __str__(self) -> str:
        return self.id

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Id):
            return self.id == o.id
        if isinstance(o, str):
            return self.id == o
        return False

    def make_combined_id(self) -> str:
        return f"{self.id}_{generate_id()}"
    

    @staticmethod
    def make():
        return Id(generate_id())
    
    @staticmethod
    def empty():
        id = Id("")
        id.id = ""
        return id
    
    def is_empty(self):
        return self.id == ""
    
    def __bool__(self) -> bool:
        return not self.is_empty()
