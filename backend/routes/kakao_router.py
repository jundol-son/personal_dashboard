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

    # ✅ 추가: 로그로 요청 정보 출력
    print("🔐 [카카오 토큰 요청 정보]")
    for k, v in data.items():
        print(f"{k}: {v}")

    res = requests.post(token_url, data=data)

    if res.status_code == 200:
        tokens = res.json()
        save_tokens(tokens)
        print("✅ Access Token 저장 완료")
        return {"message": "✅ Access Token 저장 완료", "tokens": tokens}

    print(f"❌ Token 발급 실패 | status: {res.status_code}")
    print("📩 응답 내용:", res.text)
    return {"error": "❌ Token 발급 실패", "status": res.status_code}