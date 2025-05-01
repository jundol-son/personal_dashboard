from sqlalchemy import text
from db import engine

def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS favorite_stocks (
        id SERIAL PRIMARY KEY,
        stock_name TEXT NOT NULL,
        ticker_code TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT now()
    );
    """
    with engine.connect() as conn:
        conn.execute(text(query))

def add_favorite(stock_name: str, ticker_code: str):
    query = """
    INSERT INTO favorite_stocks (stock_name, ticker_code)
    VALUES (:stock_name, :ticker_code)
    """
    try:
        with engine.connect() as conn:
            conn.execute(text(query), {"stock_name": stock_name, "ticker_code": ticker_code})
    except Exception as e:
        print("❌ 삽입 오류:", e)
        raise

def get_favorites():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, stock_name, ticker_code FROM favorite_stocks ORDER BY id DESC"))
        return [dict(row) for row in result]

def delete_favorite(id: int):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM favorite_stocks WHERE id = :id"), {"id": id})
