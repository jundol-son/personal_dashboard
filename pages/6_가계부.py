import streamlit as st
import pandas as pd

st.set_page_config(page_title="가계부", layout="wide")
st.title("💰 가계부 분석")

uploaded = st.file_uploader("📂 가계부 CSV 파일 업로드", type=["csv"])

if uploaded:
    try:
        df = pd.read_csv(uploaded)
        st.success("파일 업로드 성공!")

        if {"날짜", "분류", "항목", "금액"}.issubset(df.columns):
            st.dataframe(df)

            # 수입/지출 합계
            total = df.groupby("분류")["금액"].sum()
            st.bar_chart(total)
        else:
            st.warning("필수 컬럼: 날짜, 분류, 항목, 금액")
    except Exception as e:
        st.error(f"파일 읽기 오류: {e}")
