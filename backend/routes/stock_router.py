from fastapi import APIRouter, HTTPException
from models.stock import Stock
from services import stock_service

router = APIRouter()

@router.post("/create-table")
def create_table():
    stock_service.create_table()
    return {"message": "✅ 테이블 생성 완료"}

@router.post("/add-favorite")
def add_favorite(stock: Stock):
    stock_service.add_favorite(stock.stock_name, stock.ticker_code)
    return {"message": f"✅ {stock.stock_name} 저장 완료"}

@router.get("/get-favorites")
def get_favorites():
    return stock_service.get_favorites()

@router.delete("/delete-favorite/{id}")
def delete_favorite(id: int):
    stock_service.delete_favorite(id)
    return {"message": f"🗑️ {id}번 관심 종목 삭제됨"}
