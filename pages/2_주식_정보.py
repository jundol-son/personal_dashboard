import streamlit as st
import sys
import yfinance as yf
from datetime import date, timedelta

st.set_page_config(page_title="주식 정보", layout="wide")
st.title("📈 주식 정보 조회")
# 기본값 설정
default_symbol = "005930.KS"  # 삼성전자
symbols = st.text_input("📌 관심 종목 입력 (예: 005930.KS, AAPL, TSLA 등)", default_symbol)

# 날짜 범위 설정
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("조회 시작일", value=date.today() - timedelta(days=30))
with col2:
    end_date = st.date_input("조회 종료일", value=date.today())

if st.button("📊 조회하기"):
    try:
        stock = yf.Ticker(symbols)
        hist = stock.history(start=start_date, end=end_date)

        st.subheader("🔎 종목 정보")
        st.write(stock.info.get("longName", "정보 없음"))

        st.subheader("💹 주가 차트")
        st.line_chart(hist["Close"])

        st.subheader("📌 최근 시세 요약")
        st.dataframe(hist.tail(5))

    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류 발생: {e}")
