
from pydantic import BaseModel


class newTable(BaseModel):
    width: int
    height: int

class addShirt(BaseModel):
    size: str
    type: str
