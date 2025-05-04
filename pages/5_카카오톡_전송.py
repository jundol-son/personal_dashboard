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
    if st.button("📤 보내기"):
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {"Authorization": f"Bearer {access_token}"}
        data = {
            "object_type": "text",
            "text": msg,
            "link": {
                "web_url": "https://streamlit-dashboard-wlrq.onrender.com/카카오톡_전송",
                "mobile_web_url": "https://streamlit-dashboard-wlrq.onrender.com/카카오톡_전송"
            },
            "button_title": "📊 대시보드 열기"
        }
        res = requests.post(url, headers=headers, data={"template_object": json.dumps(data)})
        if res.status_code == 200:
            st.success("✅ 전송 성공")
        else:
            st.error(f"❌ 실패: {res.text}")