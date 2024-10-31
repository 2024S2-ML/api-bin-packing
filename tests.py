import unittest
from unittest import IsolatedAsyncioTestCase

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

        # Await the asynchronous `create_table` function
        id = await create_table(testTable)

        table: GartmentTable
        with Session(engine) as session:
            # Assuming `get_one` is a method you've defined to fetch by ID
            table = session.get(GartmentTable, id.get(id))

        self.assertEqual(id, False)

if __name__ == '__main__':
    unittest.main()
