import streamlit as st
from backend.db_user import check_user

def login_page():
    st.title("🔐 로그인")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    login_btn = st.button("로그인")

    if login_btn:
        if check_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("❌ 아이디 또는 비밀번호가 틀렸습니다.")
