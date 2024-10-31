from sqlalchemy import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.util import tables_from_leftmost

from body_dto import newTable
from models import GartmentTable


class gartmentTableService:
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def newTable(self, new_table: newTable):

        table = GartmentTable(
            width=new_table.width,
            height=new_table.height)

        with Session(self.engine) as session:
            session.add(table)
            session.commit()

        return table