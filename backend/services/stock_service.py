from sqlalchemy import text
from db import engine

def create_table():
    dbname = ""
    with engine.begin() as conn:
        # 현재 연결된 DB 이름 확인 (선택)
        dbname = conn.execute(text("SELECT current_database()")).scalar()
        print("📡 연결된 DB:", dbname)

        # 테이블 생성 실행 (결과 반환 없음)
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS favorite_stocks (
            id SERIAL PRIMARY KEY,
            stock_name TEXT NOT NULL,
            ticker_code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT now()
        );
        """))

    print("✅ 테이블 생성 완료 (DB:", dbname, ")")

def add_favorite(stock_name: str, ticker_code: str):
    query = """
    INSERT INTO favorite_stocks (stock_name, ticker_code)
    VALUES (:stock_name, :ticker_code)
    """
    try:
        with engine.begin() as conn:  # ✅ begin()으로 수정
            conn.execute(text(query), {
                "stock_name": stock_name,
                "ticker_code": ticker_code
            })
        print(f"✅ DB에 저장 완료: {stock_name} ({ticker_code})")
    except Exception as e:
        print("❌ 저장 실패:", e)
        raise

def get_favorites():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, stock_name, ticker_code FROM favorite_stocks ORDER BY id DESC"))
        return [dict(row) for row in result.mappings()]

def delete_favorite(id: int):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM favorite_stocks WHERE id = :id"), {"id": id})
