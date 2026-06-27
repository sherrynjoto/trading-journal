from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json, os

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
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_trades(trades):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(trades, f)
    except:
        pass

@app.get("/")
def root():
    return {"status": "Trading Journal API is running"}

@app.post("/trade")
async def add_trade(request: Request):
    try:
        trade = await request.json()
        trades = load_trades()
        trade["id"] = len(trades) + 1
        trades.append(trade)
        save_trades(trades)
        return {"message": "Trade saved", "id": trade["id"]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/trades")
def get_trades():
    return load_trades()

@app.delete("/trades")
def clear_trades():
    save_trades([])
    return {"message": "Cleared"}
