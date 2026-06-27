from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

@app.get("/")
def root():
    return {"status": "Trading Journal API is running"}

@app.post("/trade")
async def add_trade(request: Request):
    try:
        trade = await request.json()
        trade.pop("id", None)
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{SUPABASE_URL}/rest/v1/trades",
                headers=headers(),
                json=trade
            )
        return {"message": "Trade saved", "data": res.json()}
    except Exception as e:
        return {"error": str(e)}

@app.get("/trades")
async def get_trades():
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{SUPABASE_URL}/rest/v1/trades?order=open_time.asc&limit=10000",
                headers=headers()
            )
        return res.json()
    except Exception as e:
        return {"error": str(e)}

@app.delete("/trades")
async def clear_trades():
    try:
        async with httpx.AsyncClient() as client:
            await client.delete(
                f"{SUPABASE_URL}/rest/v1/trades?id=gte.0",
                headers=headers()
            )
        return {"message": "Cleared"}
    except Exception as e:
        return {"error": str(e)}
