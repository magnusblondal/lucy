

from pydantic import BaseModel
import shortuuid

def generate_id():
    return shortuuid.ShortUUID().random(length=10)


class Foo(BaseModel):
    a: int
    s: str = None

    def __init__(self, a: int, s: str = None) -> None:
        self.a = a

print(Foo(1).dict())