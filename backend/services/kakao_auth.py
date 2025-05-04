import os
import json
import requests
from sqlalchemy import create_engine, text

CLIENT_ID = "48f8318d48bafe040f2d9605f68bf6bb"
token_path = os.path.join(os.getcwd(), "token.json")

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# ✅ DB에 토큰 저장
def save_tokens(tokens: dict):
    with engine.connect() as conn:
        conn.execute(
            text("""
            INSERT INTO kakao_token (access_token, refresh_token)
            VALUES (:access_token, :refresh_token)
            """),
            {
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"]
            }
        )
        conn.commit()

# ✅ 기존 로컬 JSON 방식 (보존용)
def load_access_token_from_file():
    if not os.path.exists(token_path):
        return None
    with open(token_path, "r") as f:
        tokens = json.load(f)
    return tokens.get("access_token")

# ✅ 새로 추가된 DB 기반 토큰 로딩 방식
def load_access_token():
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT access_token FROM kakao_token ORDER BY created_at DESC LIMIT 1")
            ).fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"❌ DB에서 토큰 불러오기 실패: {e}")
        return None

def refresh_access_token():
    if not os.path.exists(token_path):
        return None
    with open(token_path, "r") as f:
        tokens = json.load(f)
    refresh_token = tokens.get("refresh_token")
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "refresh_token": refresh_token,
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        new_tokens = response.json()
        save_tokens({**tokens, **new_tokens})
        return new_tokens.get("access_token")
    return None
