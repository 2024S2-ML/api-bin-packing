import json
import pickle
from io import BytesIO
import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import FileResponse, StreamingResponse

from Utils import Utils
from body_dto import newTable, addShirt, ShirtCreate
from models import Base, GartmentTable, Shirt, ShirtRects
from packing_layer import Packer
from services import GartmentTableService, ShirtService, ShirtRectsService, PackerService
from temp_content import get_rects, plot_bin_packing

# iniciar DB
engine = create_engine("sqlite:///database.db", echo=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello_world_root():
    return {"Hello": "World"}

@app.post('/table/new')
async def create_table(new_table: newTable):

    tableService = GartmentTableService(engine)
    tableId = tableService.newTable(new_table)

    return json.dumps({"id": tableId})

@app.get('/table/{table_id}')
async def get_table(table_id: int):
    tableService = GartmentTableService(engine)
    table = tableService.get_table(table_id)

    return Utils.mount_table_return(table)

@app.post('/table/{table_id}/add')
async def add_rect(table_id: int, add_shirt: addShirt):

    tableService = GartmentTableService(engine)
    table = tableService.get_table(table_id)

    shirtService = ShirtService(engine)
    shirt = shirtService.get_by_size_type(add_shirt.size, add_shirt.type)

    shirtRectsService = ShirtRectsService(engine)
    shirtRects = shirtRectsService.get_by_shirtId(shirt.id)

    if table is not None and shirt is not None and shirtRects is not None:
        rectsList = shirtRectsService.transform_into_rects(shirtRects)


        pack = Packer((table.width, table.height))

        packerService = PackerService(engine)
        loaded_packer = None
        if table.bin_maxrects is not None:
            tableService.update_table(pack, table)

        pack.add_many(rectsList)
        pack.pack()

        table.bin_skyline = pack.get_packer_sky().rect_list().__str__()
        table.bin_guillotine = pack.get_packer_gui().rect_list().__str__()
        table.bin_maxrects = pack.get_packer_max().rect_list().__str__()

        tableService.save(table)

        #if loaded_packer is not None:
        #    loaded_packer.state = pickle.dumps(pack)
        #    packerService.save(loaded_packer)
        #else:
        #    packerService.new(pack, table.id)


        return Utils.mount_table_return(table)

    return json.dumps({"error": "Error during the addition"})




@app.post("/shirts/", response_model=ShirtCreate)
def create_shirt(shirt: ShirtCreate):

    with Session(engine) as session:
        db_shirt = Shirt(type=shirt.type, size=shirt.size)
        session.add(db_shirt)
        session.commit()
        session.refresh(db_shirt)

        for rect in shirt.shirt_rects:
            db_rect = ShirtRects(width=rect.width, height=rect.height, shirt_id=db_shirt.id)
            session.add(db_rect)
        session.commit()

    return db_shirt



@app.delete("/shirts/{shirt_id}")
def delete_shirt(shirt_id: int):
    with Session(engine) as session:
        db_shirt = session.query(Shirt).filter(Shirt.id == shirt_id).first()
        if db_shirt is None:
            raise HTTPException(status_code=404, detail="Shirt not found")
        session.delete(db_shirt)
        session.commit()

    return {"message": "Shirt deleted successfully"}

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