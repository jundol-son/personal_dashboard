import streamlit as st
import yfinance as yf
from datetime import date, timedelta

st.set_page_config(page_title="주식 정보", layout="wide")
st.title("📈 주식 정보 대시보드")

# 간단한 종목 검색 힌트
stock_list = {
    "삼성전자": "005930.KS",
    "카카오": "035720.KQ",
    "현대차": "005380.KS",
    "애플(Apple)": "AAPL",
    "테슬라(Tesla)": "TSLA",
    "마이크로소프트(MSFT)": "MSFT"
}

stock_name = st.selectbox("📌 관심 종목 선택 (또는 코드 직접 입력)", list(stock_list.keys()) + ["직접 입력"])

if stock_name == "직접 입력":
    symbol = st.text_input("종목 코드 입력 (예: 005930.KS, AAPL)", "AAPL")
else:
    symbol = stock_list[stock_name]

# 날짜 범위
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("조회 시작일", value=date.today() - timedelta(days=30))
with col2:
    end_date = st.date_input("조회 종료일", value=date.today())

# 조회 버튼
if st.button("📊 주식 데이터 조회"):
    try:
        ticker = yf.Ticker(symbol)

        # 데이터를 가볍게 불러오도록 period 사용
        hist = ticker.history(start=start_date, end=end_date)
        info = ticker.info

        # 종목 정보 요약 표시
        st.subheader("📘 종목 정보")
        st.markdown(f"**종목명**: {info.get('longName', '정보 없음')}")
        st.markdown(f"**산업**: {info.get('sector', 'N/A')} / {info.get('industry', 'N/A')}")
        st.markdown(f"**시가총액**: {info.get('marketCap', 'N/A'):,} USD")
        st.markdown(f"**배당 수익률**: {info.get('dividendYield', 0) * 100:.2f}%")

        # 차트
        st.subheader("💹 종가 차트")
        st.line_chart(hist["Close"])

        # 최근 5일 시세
        st.subheader("📌 최근 시세 (마지막 5일)")
        st.dataframe(hist.tail(5))

    except Exception as e:
        st.error(f"❌ 데이터 조회 중 오류 발생: {e}")
