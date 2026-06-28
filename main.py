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

SUPABASE_URL = "https://hirvwvmctmgsjweedonk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhpcnZ3dm1jdG1nc2p3ZWVkb25rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI1NjA5OTUsImV4cCI6MjA5ODEzNjk5NX0.A406IYAEvpCGgtsBgYigzU3Gpm6GS0B8u1a9NHW7Gpg"

def get_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

@app.get("/")
def root():
    return {"status": "Trading Journal API is running"}

@app.get("/debug")
def debug():
    return {
        "supabase_url": SUPABASE_URL,
        "key_length": len(SUPABASE_KEY)
    }

@app.post("/trade")
async def add_trade(request: Request):
    try:
        trade = await request.json()
        trade.pop("id", None)
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{SUPABASE_URL}/rest/v1/trades",
                headers=get_headers(),
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
                headers=get_headers()
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
                headers=get_headers()
            )
        return {"message": "Cleared"}
    except Exception as e:
        return {"error": str(e)}
