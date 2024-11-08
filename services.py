import pickle
import uuid
import time
from operator import and_
from typing import List, Tuple

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.util import tables_from_leftmost

from body_dto import newTable
from models import GartmentTable, Shirt, ShirtRects, PackerModel
from packing_layer import Packer


class GartmentTableService:
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def newTable(self, new_table: newTable):

        table = GartmentTable(
            width=new_table.width,
            height=new_table.height)

        tabId = self.save(table)

        return tabId

    def save(self, table: GartmentTable):
        with Session(self.engine) as session:
            session.add(table)

            session.flush()
            tabId = table.id
            session.commit()
            session.refresh(table)

            return tabId

    def get_table(self, tabId: int):

        table: GartmentTable

        with Session(self.engine) as session:
            table = session.get(GartmentTable, tabId)

            return table


class ShirtService:
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def new(self):
        raise NotImplementedError()

    def get_by_size_type(self, size: str, type: str) -> Shirt:
        shirt: Shirt

        with Session(self.engine) as session:
            stmt = select(Shirt).where(and_(Shirt.size == size, Shirt.type == type))
            shirt = session.execute(stmt).scalar()

            return shirt

    def get_one(self, obj_id: int) -> Shirt:
        shirt: Shirt

        with Session(self.engine) as session:
            shirt = session.get(Shirt, obj_id)

            return shirt


class ShirtRectsService:
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def new(self):
        raise NotImplementedError()

    def get_by_shirtId(self, shirt_id: int) -> List[ShirtRects]:
        shirtRects: List[ShirtRects]

        with Session(self.engine) as session:
            stmt = select(ShirtRects).where(ShirtRects.shirt_id == shirt_id)
            shirtRects = session.execute(stmt).scalars().all()

            return shirtRects

    def transform_into_rects(self, shirtRects: List[ShirtRects]) -> List[Tuple[int, int, str]]:
        result = []
        for rect in shirtRects:
            unique_id = self.generate_uuid(rect.id, rect.shirt_id)
            result.append((rect.width, rect.height, unique_id))

        return result


    def generate_uuid(self, rect_id: int, shirt_id: int) -> str:
        timestamp = str(int(time.time()))
        unique_string = f"{rect_id}{shirt_id}{timestamp}"

        return str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_string))

class PackerService:
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def new(self, packer: Packer, tableId):
        packer_model = PackerModel(packer)
        packer_model.table_id = tableId

        with Session(self.engine) as session:
            session.add(packer_model)
            session.commit()

    def save(self, packer_model: PackerModel):
        with Session(self.engine) as session:
            session.add(packer_model)
            session.commit()

    def get_by_tableId(self, table_id: int) -> PackerModel:
        packer: PackerModel

        with Session(self.engine) as session:
            stmt = select(PackerModel).where(PackerModel.table_id == table_id)
            packer = session.execute(stmt).scalars().first()

            return packer

    def get_packer_instance(self, packer: PackerModel):
        return pickle.loads(packer.state)