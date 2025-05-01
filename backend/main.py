from fastapi import FastAPI
from db import get_db_version

app = FastAPI()

@app.get("/")
def root():
    return {"message": "✅ FastAPI is running"}

@app.get("/db")
def db_check():
    version = get_db_version()
    return {"db_version": version}
