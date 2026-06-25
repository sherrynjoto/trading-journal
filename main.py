from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json, os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "trades.json"

def load_trades():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_trades(trades):
    with open(DB_FILE, "w") as f:
        json.dump(trades, f)

class Trade(BaseModel):
    symbol: str
    direction: str
    open_time: str
    close_time: str
    entry: float
    exit: float
    lots: float
    pnl: float

@app.get("/")
def root():
    return {"status": "Trading Journal API is running"}

@app.post("/trade")
def add_trade(trade: Trade):
    trades = load_trades()
    trade_dict = trade.dict()
    trade_dict["date"] = trade.open_time[:10]
    trade_dict["id"] = len(trades) + 1
    trades.append(trade_dict)
    save_trades(trades)
    return {"message": "Trade saved", "id": trade_dict["id"]}

@app.get("/trades")
def get_trades():
    return load_trades()

@app.delete("/trades")
def clear_trades():
    save_trades([])
    return {"message": "All trades cleared"}
