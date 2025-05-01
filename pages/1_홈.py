import streamlit as st
from datetime import datetime

st.title("🏠 홈")
st.write(f"📅 오늘은 {datetime.today().strftime('%Y-%m-%d')} 입니다.")
st.info("이곳은 대시보드 메인 요약 페이지입니다.")
