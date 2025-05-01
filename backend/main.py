from fastapi import FastAPI
from db import get_db_version
from routes.stock_router import router as stock_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "✅ FastAPI is running"}

@app.get("/db")
def db_check():
    version = get_db_version()
    return {"db_version": version}

app.include_router(stock_router)
