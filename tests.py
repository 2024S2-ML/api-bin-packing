import json
import unittest
from unittest import IsolatedAsyncioTestCase

from matplotlib.font_manager import json_load
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from body_dto import newTable
from main import create_table, add_rect, remove_shirt
from models import GartmentTable
from services import PackerService, GartmentTableService


class garmentTable(IsolatedAsyncioTestCase):
    async def test_create(self):
        engine = create_engine("sqlite:///database.db", echo=True)

        testTable =  type("", (), {})()
        testTable.width = 800
        testTable.height = 600

        id = json.loads(await create_table(testTable))
        id = id.get("id")

        table: GartmentTable
        with Session(engine) as session:
            table = session.get(GartmentTable, id)

            self.assertEqual(id, table.id)

    async def test_addShirt(self):
        engine = create_engine("sqlite:///database.db", echo=True)

        addStmt = type("", (), {})()
        addStmt.size = "P"
        addStmt.type = "P"

        tableId = 1
        with Session(engine) as session:
            table = session.get(GartmentTable, tableId)


        table_updated = json.loads(await add_rect(tableId, addStmt))

        assert table.bin_maxrects != table_updated["maxRects"]
        assert table.bin_skyline != table_updated["skyline"]
        assert table.bin_guillotine != table_updated["guillotine"]


    async def test_removeShirt(self):
        engine = create_engine("sqlite:///database.db", echo=True)

        tableId = 1
        tableService = GartmentTableService(engine)
        table = tableService.get_table(tableId)

        shirt_id = table.max_rects_array[0][-1].split('.')[-1]

        table_updated = await remove_shirt(tableId, shirt_id)

        # n to sabendo fazer as comparações direito, mas ta funfando
        assert shirt_id not in table_updated["maxRects"]
        assert shirt_id not in table_updated["skyline"]
        assert shirt_id not in table_updated["guillotine"]


if __name__ == '__main__':
    unittest.main()
