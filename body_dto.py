from typing import List

from pydantic import BaseModel


class newTable(BaseModel):
    width: int
    height: int

class addShirt(BaseModel):
    size: str
    type: str

class ShirtRectCreate(BaseModel):
    width: int
    height: int

class ShirtCreate(BaseModel):
    type: str
    size: str
    shirt_rects: List[ShirtRectCreate] = []