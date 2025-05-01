import streamlit as st
import requests

st.set_page_config(page_title="카카오톡 메시지", layout="wide")
st.title("💬 카카오톡 메시지 전송")

access_token = st.text_input("🔑 액세스 토큰 입력", type="password")
message = st.text_area("📨 보낼 메시지 내용", "안녕하세요! 대시보드에서 보냅니다.")

if st.button("📤 카카오톡 보내기"):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "template_object": {
            "object_type": "text",
            "text": message,
            "link": {"web_url": "http://localhost", "mobile_web_url": "http://localhost"},
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        st.success("메시지 전송 성공 ✅")
    else:
        st.error(f"전송 실패 ❌ : {response.json()}")
