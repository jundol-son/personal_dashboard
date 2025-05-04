from fastapi import APIRouter
import requests
from services.kakao_auth import save_tokens

CLIENT_ID = "48f8318d48bafe040f2d9605f68bf6bb"
REDIRECT_URI = "https://fastapi-backend-io09.onrender.com/callback"

router = APIRouter()

@router.get("/callback")
def kakao_callback(code: str):
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    res = requests.post(token_url, data=data)
    if res.status_code == 200:
        tokens = res.json()
        save_tokens(tokens)
        return {"message": "✅ Access Token 저장 완료", "tokens": tokens}
    return {"error": "❌ Token 발급 실패", "status": res.status_code}
