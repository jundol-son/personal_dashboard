import streamlit as st
from datetime import date, timedelta
import pandas as pd
import FinanceDataReader as fdr
from yahooquery import Ticker
from utils.favorite_api import add_favorite_to_db, get_favorite_stocks

st.set_page_config(page_title="📈 주식 정보", layout="wide")
st.title("📈 주식 정보 대시보드")

# 종목 목록 불러오기 (한국 종목만 우선)
@st.cache_data(ttl=86400)
def load_korea_stock_list():
    df = fdr.StockListing('KRX')
    df = df[['Name', 'Symbol']]
    df['Display'] = df['Name'] + " (" + df['Symbol'] + ")"
    return df

krx_df = load_korea_stock_list()
symbols = krx_df['Display'].tolist()
symbols.insert(0, "직접 입력 (미국 종목 등)")

# 종목 선택
selected = st.selectbox("📌 관심 종목 선택 (또는 직접 입력)", options=symbols)
if selected == "직접 입력 (미국 종목 등)":
    manual_symbol = st.text_input("미국 종목 코드를 직접 입력 (예: AAPL, TSLA 등)", "")
else:
    manual_symbol = krx_df[krx_df["Display"] == selected]["Symbol"].values[0]

# 날짜 입력
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("조회 시작일", value=date.today() - timedelta(days=30))
with col2:
    end_date = st.date_input("조회 종료일", value=date.today())

# 캐시된 조회 함수
@st.cache_data(ttl=3600)
def get_stock_data(symbol, start, end):
    if symbol.isdigit():  # 한국 종목
        df = fdr.DataReader(symbol, start, end)
        info = f"{symbol} (Korean Stock)"
    else:
        stock = Ticker(symbol)
        info = stock.summary_detail.get(symbol, {}).get("longName", "정보 없음")
        df = stock.history(start=start, end=end)
        df = df[df.index.get_level_values(0) == symbol]
        df = df.reset_index().set_index("date")
    return info, df

# 버튼 클릭 시 조회
if st.button("📊 조회하기") and manual_symbol:
    try:
        info, hist = get_stock_data(manual_symbol, start_date, end_date)
        st.subheader(f"🔎 선택된 종목: {info}")
        st.line_chart(hist["close"] if "close" in hist else hist["Close"])
        st.dataframe(hist.tail(5))

        # 종목 즐겨찾기 버튼 추가
        if "Korean Stock" in info:
            stock_name = selected.split(" (")[0]
            ticker_code = manual_symbol
        else:
            stock_name = info
            ticker_code = manual_symbol.upper()

        if st.button("⭐ 관심 종목으로 등록"):
            status, result = add_favorite_to_db(stock_name, ticker_code)
            if status == 200:
                st.success("✅ 관심 종목으로 등록 완료!")
            else:
                st.error(f"등록 실패: {result}")

    except Exception as e:
        st.error(f"❌ 데이터 조회 중 오류 발생: {e}")

# 관심 종목 목록 표시
st.divider()
st.subheader("⭐ 등록된 관심 종목")
status, favorites = get_favorite_stocks()
if status == 200 and favorites:
    df = pd.DataFrame(favorites)
    st.dataframe(df)
else:
    st.info("아직 등록된 관심 종목이 없습니다.")
