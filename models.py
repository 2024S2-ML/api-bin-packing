from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
     pass

class GartmentTable(Base):
    __tablename__ = "gartment_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    bin: Mapped[str] = mapped_column(String(200))

class Shirt(Base):
    __tablename__ = "shirt"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50))
    size: Mapped[str] = mapped_column(String(3))
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)