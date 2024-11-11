import ast
import json
import dill
import uuid
import time
from operator import and_
from typing import List, Tuple

from matplotlib.font_manager import json_dump
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

    def save(self, table: GartmentTable, pack: Packer = None):

        if pack is not None:
            table.bin_skyline = pack.get_packer_sky().rect_list().__str__()
            table.bin_guillotine = pack.get_packer_gui().rect_list().__str__()
            table.bin_maxrects = pack.get_packer_max().rect_list().__str__()

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

            if table is not None:
                self.table_array_transform(table)

            return table

    def remove_shirt(self, table_id: int, random_shirt_id: int):
        table = self.get_table(table_id)

        GartmentTableService.table_array_transform(table)
        GartmentTableService.remove_rect(table, random_shirt_id)

        pack = Packer(bin=(table.width, table.height))

        self.update_packer(pack, table)

        pack.pack()
        packer_service = PackerService(self.engine, table.id)
        packer_service.save(pack)

        self.save(table, pack)

        return table


    @staticmethod
    def remove_rect(table: GartmentTable, random_shirt_id: int):
        table.max_rects_array = [item for item in table.max_rects_array if random_shirt_id.__str__() not in item[-1]]
        table.skyline_array = [item for item in table.skyline_array if random_shirt_id.__str__() not in item[-1]]
        table.guillotine_array = [item for item in table.guillotine_array if random_shirt_id.__str__() not in item[-1]]

    @staticmethod
    def table_array_transform(table: GartmentTable):
        if table.bin_maxrects is not None:
            table.max_rects_array = ast.literal_eval(table.bin_maxrects)
        if table.bin_skyline is not None:
            table.skyline_array = ast.literal_eval(table.bin_skyline)
        if table.bin_guillotine is not None:
            table.guillotine_array = ast.literal_eval(table.bin_guillotine)

    @staticmethod
    def update_packer(packer: Packer, table: GartmentTable):
        packer.get_packer_max()._avail_rect = [item[-3:] for item in table.max_rects_array]
        packer.get_packer_sky()._avail_rect = [item[-3:] for item in table.skyline_array]
        packer.get_packer_gui()._avail_rect = [item[-3:] for item in table.guillotine_array]



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

    def transform_into_rects(self, shirtRects: List[ShirtRects], random_id: int = uuid.uuid4().int >> 32) -> List[Tuple[int, int, str]]:
        result = []
        for rect in shirtRects:
            unique_id = self.generate_uuid(rect.id, rect.shirt_id, random_id)
            result.append((rect.width, rect.height, unique_id))

        return result


    def generate_uuid(self, rect_id: int, shirt_id: int, random_id: int = 0) -> str:
        #timestamp = str(int(time.time()))
        unique_string = f"{rect_id}.{shirt_id}.{random_id}"
        #uu = uuid.uuid5(uuid.NAMESPACE_DNS, unique_string)
        return str(unique_string)

class PackerService:
    engine: Engine
    loaded_packer: PackerModel = None

    def __init__(self, engine: Engine, tableId: int = None):
        self.engine = engine

        if tableId is not None:
            self.loaded_packer = self.get_by_tableId(tableId)

    def new(self, packer: Packer, tableId):
        packer_model = PackerModel(packer)
        packer_model.table_id = tableId

        with Session(self.engine) as session:
            session.add(packer_model)
            session.commit()

    def save(self, packer: Packer):
        self.set_packer_instance(packer, self.loaded_packer)

        with Session(self.engine) as session:
            session.add(self.loaded_packer)
            session.commit()

    def get_by_tableId(self, table_id: int) -> PackerModel:
        packer: PackerModel

        with Session(self.engine) as session:
            stmt = select(PackerModel).where(PackerModel.table_id == table_id)
            packer = session.execute(stmt).scalars().first()
            self.loaded_packer = packer

            return packer

    def get_packer(self, table):
        self.loaded_packer = self.get_by_tableId(table.id)
        pack = self.get_packer_instance(self.loaded_packer)

        return pack

    @staticmethod
    def get_packer_instance(packer: PackerModel) -> Packer:
        packer_max = dill.loads(packer.state_max)
        packer_sky = dill.loads(packer.state_sky)
        packer_gui = dill.loads(packer.state_gui)

        packer_return = Packer(packer_max=packer_max, packer_sky=packer_sky, packer_gui=packer_gui)

        return packer_return

    @staticmethod
    def set_packer_instance(packer: Packer, packer_model: PackerModel) -> PackerModel:
        packer_model.state_max = dill.dumps(packer._packer_sky)
        packer_model.state_sky = dill.dumps(packer._packer_gui)
        packer_model.state_gui = dill.dumps(packer._packer_max)

        return packer_model