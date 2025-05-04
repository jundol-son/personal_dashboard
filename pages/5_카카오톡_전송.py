import streamlit as st
import requests
import json
from backend.services.kakao_auth import load_access_token

st.set_page_config(page_title="카카오톡 메시지", layout="centered")
st.title("📨 카카오톡 나에게 메시지 보내기")

access_token = load_access_token()
if not access_token:
    st.warning("❗ Access Token이 없습니다. FastAPI /callback을 통해 로그인해 주세요.")
else:
    msg = st.text_area("보낼 메시지", "안녕하세요, 자동화 테스트입니다!")

    streamlit_url = "https://streamlit-dashboard-wlrq.onrender.com"

    if st.button("📤 보내기"):
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # ✅ 카카오 템플릿 구조 정확히 맞추기
        data = {
            "object_type": "text",
            "text": msg,
            "link": {
                "web_url": streamlit_url,
                "mobile_web_url": streamlit_url
            },
            "button_title": "📊 대시보드 열기"
        }

        payload = {
            "template_object": json.dumps(data, ensure_ascii=False)
        }

        res = requests.post(url, headers=headers, data=payload)

        if res.status_code == 200:
            st.success("✅ 전송 성공")
        else:
            st.error(f"❌ 실패: {res.status_code} - {res.text}")
