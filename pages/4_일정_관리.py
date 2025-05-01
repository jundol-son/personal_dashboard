import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="일정 관리", layout="wide")
st.title("📅 일정 등록")

if "schedules" not in st.session_state:
    st.session_state["schedules"] = []

with st.form("schedule_form"):
    title = st.text_input("일정 제목")
    date = st.date_input("일자", value=datetime.today())
    time = st.time_input("시간", value=datetime.now().time())
    note = st.text_area("메모", "")

    submitted = st.form_submit_button("✅ 일정 추가")
    if submitted:
        st.session_state["schedules"].append({
            "title": title,
            "datetime": datetime.combine(date, time),
            "note": note
        })
        st.success("일정이 추가되었습니다.")

st.subheader("📋 등록된 일정 목록")
for s in st.session_state["schedules"]:
    st.write(f"- **{s['title']}** ({s['datetime'].strftime('%Y-%m-%d %H:%M')})")
    if s['note']:
        st.caption(f"📌 {s['note']}")
