from typing import List
import json
import argparse

from fastapi import FastAPI
from model import Model
from pydantic import BaseModel, RootModel, model_serializer
import uvicorn

from db_utils import insert_request

class Item(BaseModel):
    data: str

    @model_serializer(return_type=dict)
    def parse_data(self):
        data = json.loads(self.data)
        return data


class ItemList(RootModel):
    root: List[Item]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


app = FastAPI()
model = Model(1, 2, 3)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict")
def read_item(item_list: ItemList):
    item_list = [item.model_dump(mode='json') for item in item_list]
    return [{
        "EVENT_ID": item["EVENT_ID"],
        "LABEL_PRED": model.predict(**item)
    } for item in item_list]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_port',
                        default=5432,
                        type=int,
                        help='database port, 5432 by default')
    parser.add_argument('--server_port',
                        default=8000,
                        type=int,
                        help='server port, 8000 by default')
    args = parser.parse_args()
    uvicorn.run("app:app", host='127.0.0.1', port=args.server_port, reload=True)
