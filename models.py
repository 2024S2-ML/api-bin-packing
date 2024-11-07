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
    bin_maxrects: Mapped[int] = mapped_column(String(400), nullable=True)
    bin_skyline: Mapped[str] = mapped_column(String(400), nullable=True)
    bin_guillotine: Mapped[str] = mapped_column(String(400), nullable=True)

class Shirt(Base):
    __tablename__ = "shirt"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50))
    size: Mapped[str] = mapped_column(String(3)) # pp p m g gg

    shirt_rects: Mapped[List["ShirtRects"]] = relationship(
        "ShirtRects", back_populates="shirt", cascade="all, delete-orphan"
    )

class ShirtRects(Base):
    __tablename__ = "shirt_rects"

    id: Mapped[int] = mapped_column(primary_key=True)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    shirt_id: Mapped[str] = mapped_column(ForeignKey("shirt.id"))

    shirt: Mapped["Shirt"] = relationship("Shirt", back_populates="shirt_rects")
