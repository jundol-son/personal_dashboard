from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from db import get_db_version
from routes.stock_router import router as stock_router

app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])  # ✅ GET + HEAD 모두 허용
def root(request: Request):
    if request.method == "HEAD":
        return JSONResponse(status_code=200)
    return {"message": "Hello from FastAPI"}

@app.get("/db")
def db_check():
    version = get_db_version()
    return {"db_version": version}

app.include_router(stock_router)
