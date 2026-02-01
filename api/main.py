from fastapi import FastAPI
from pydantic import BaseModel
from hashlib import sha256
from .ml_model import predict
from .blockchain import send_to_chain
import json


app = FastAPI()

class Transaction(BaseModel):
    BlockHeight: int
    TimeStamp: float
    Value: float
    From: str
    To: str

@app.post("/process")
def process(tx: Transaction):
    tx_dict = tx.dict()
    pred = predict(tx_dict)
    h = sha256(str(tx_dict).encode()).hexdigest()
    tx_hash = send_to_chain(pred, h)
    return {
        "input": tx_dict,
        "prediction": pred,
        "hash": h,
        "tx_hash": tx_hash
    }
