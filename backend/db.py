import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# .env 파일 로딩
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL 환경변수가 설정되지 않았습니다.")
    raise ValueError("DATABASE_URL 환경변수가 없음")

try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    print("❌ DB 엔진 생성 실패:", e)
    raise

def get_db_version():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            return result.fetchone()[0]
    except Exception as e:
        print("❌ DB 연결 실패:", e)
        raise
