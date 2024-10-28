from io import BytesIO

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.models import Response
from sqlalchemy import create_engine
from sqlalchemy.dialects.mssql import IMAGE
from sqlalchemy.orm import Session
from starlette.responses import FileResponse, StreamingResponse

from models import Base
from packing_layer import Packer
from temp_content import get_rects, plot_bin_packing

# iniciar DB
engine = create_engine("sqlite:///database.db", echo=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def hello_world_root():
    return {"Hello": "World"}

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