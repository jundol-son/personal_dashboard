import streamlit as st
from login import login_page

# 로그인 세션 상태 초기화
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 로그인하지 않았다면 로그인 페이지 보여주기
if not st.session_state.authenticated:
    login_page()
    st.stop()

st.set_page_config(page_title="개인 통합 대시보드", layout="wide")
st.title("📊 개인 통합 대시보드")
st.markdown("좌측 사이드바에서 기능을 선택하세요.")
