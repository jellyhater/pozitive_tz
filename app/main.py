from typing import List
import json
import argparse

from fastapi import FastAPI
from model import HTTPRequestClassifier
from pydantic import BaseModel, RootModel, model_serializer
import uvicorn
from db_utils import Database
from config import Config


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
model = HTTPRequestClassifier(
    weights_path="./model/weights/svm.pkl"
)
config = Config()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict")
def read_item(item_list: ItemList):
    # init db connection if flag True
    db = Database(db_port=config.db_port, user=config.postgres_user, password=config.postgres_password) \
        if config.postgres_logging else None
    # jsonify Item objects
    item_list = [item.model_dump(mode='json') for item in item_list]

    for item in item_list:
        # get prediction
        item["LABEL_PRED"] = model(item)
        # insert if db initialized
        if db:
            db.insert(
                event_id=item["EVENT_ID"],
                client_ip=item["CLIENT_IP"],
                client_useragent=item["CLIENT_USERAGENT"],
                request_size=item["REQUEST_SIZE"],
                response_code=item["RESPONSE_CODE"],
                matched_variable_src=item["MATCHED_VARIABLE_SRC"],
                matched_variable_name=item["MATCHED_VARIABLE_NAME"],
                matched_variable_value=item["MATCHED_VARIABLE_VALUE"],
                label_pred=item["LABEL_PRED"]
            )

    return [{
        "EVENT_ID": item["EVENT_ID"],
        "LABEL_PRED": item["LABEL_PRED"]
    } for item in item_list]


@app.get("/history")
def get_queries():
    db = Database(db_port=config.db_port, user=config.postgres_user, password=config.postgres_password) \
        if config.postgres_logging else None
    result = db.select()
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host=config.server_host, port=config.server_port, reload=True)
