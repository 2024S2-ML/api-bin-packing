import pickle
from typing import List
from sqlalchemy import ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

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

    packers: Mapped[List["PackerModel"]] = relationship(
        "PackerModel", back_populates="table", cascade="all, delete-orphan"
    )

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

class PackerModel(Base):
    __tablename__ = 'packers'
    id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[bytes] = mapped_column(LargeBinary)
    table_id: Mapped[int] = mapped_column(ForeignKey("gartment_table.id"))

    # Make sure this matches the relationship in GartmentTable
    table: Mapped["GartmentTable"] = relationship("GartmentTable", back_populates="packers")

    def __init__(self, packer_instance):
        self.state = pickle.dumps(packer_instance)
