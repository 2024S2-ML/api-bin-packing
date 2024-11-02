import json
from io import BytesIO
import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session

from starlette.responses import FileResponse, StreamingResponse

from body_dto import newTable, addShirt
from models import Base, GartmentTable
from packing_layer import Packer
from services import GartmentTableService, ShirtService, ShirtRectsService
from temp_content import get_rects, plot_bin_packing

# iniciar DB
engine = create_engine("sqlite:///database.db", echo=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def hello_world_root():
    return {"Hello": "World"}

@app.post('/table/new')
async def create_table(new_table: newTable):

    tableService = GartmentTableService(engine)
    tableId = tableService.newTable(new_table)

    return json.dumps({"id": tableId})

@app.post('/table/{table_id}/add')
async def add_rect(table_id: int, add_shirt: addShirt):

    tableService = GartmentTableService(engine)
    table = tableService.get_table(table_id)

    shirtService = ShirtService(engine)
    shirt = shirtService.get_by_size_type(add_shirt.size, add_shirt.type)

    shirtRectsService = ShirtRectsService(engine)
    shirtRects = shirtRectsService.get_by_shirtId(shirt.shirtId)

    if table is not None and shirt is not None:
        pack = Packer((table.width, table.height))
        pack.add_rect(shirt.width, s)
        pack.pack()


    return json.dumps({"id": tableId})

## TEMP AREA
@app.get('/pack')
def pack_path():
    pack = Packer((800, 500))
    pack.add_many(get_rects())
    pack.pack()

    return {
        "maxreacts": pack._packer_max.rect_list(),
        "guilhotine":pack._packer_gui.rect_list(),
        "skyline":pack._packer_sky.rect_list()
    }

@app.get(
    '/packImage',
    )
def pack_path():

    pack = Packer((800, 500))
    pack.add_many(get_rects())
    pack.pack()

    plt = plot_bin_packing(pack._packer_max.rect_list(), pack.bin)

    # Tranformar o grafico em imagem
    image_data = BytesIO()
    plt.savefig(image_data, format='png')
    image_data.seek(0)
    plt.close()


    return StreamingResponse(image_data, media_type="image/png")

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)