from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes.stock_router import router as stock_router
from routes.kakao_router import router as kakao_router
from db import get_db_version
import requests
import os
from backend.services.kakao_auth import save_tokens  # access_token 저장용 함수

app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])
def root(request: Request):
    if request.method == "HEAD":
        return JSONResponse(status_code=200)

    # 🔐 카카오 OAuth 인가 코드가 있는 경우 처리
    code = request.query_params.get("code")
    if code:
        token_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": os.environ.get("KAKAO_REST_API_KEY"),
            "redirect_uri": os.environ.get("KAKAO_REDIRECT_URI"),
            "code": code,
        }

        print("🔐 [카카오 토큰 요청 정보]")
        for k, v in data.items():
            print(f"{k}: {v}")

        res = requests.post(token_url, data=data)

        if res.status_code == 200:
            tokens = res.json()
            save_tokens(tokens)
            print("✅ Access Token 저장 완료")
            return {"message": "✅ Access Token 저장 완료", "tokens": tokens}
        else:
            print("❌ Token 발급 실패:", res.text)
            return {"error": "❌ Token 발급 실패", "status": res.status_code}

    # 기본 응답 (keepalive 용)
    return {"message": "Hello from FastAPI"}

@app.get("/db")
def db_check():
    version = get_db_version()
    return {"db_version": version}

# 📦 라우터 등록
app.include_router(stock_router)
app.include_router(kakao_router)
