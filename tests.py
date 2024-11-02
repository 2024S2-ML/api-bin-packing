import json
import unittest
from unittest import IsolatedAsyncioTestCase

from matplotlib.font_manager import json_load
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from body_dto import newTable
from main import create_table
from models import GartmentTable

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

if __name__ == '__main__':
    unittest.main()
