import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
from yahooquery import Ticker
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="📈 주식 및 금리 정보", layout="wide")
st.title("📈 한국 주식 + 미국/한국 국채 금리 대시보드")

# -------------------- 한국 종목 목록 --------------------
@st.cache_data(ttl=86400)
def load_korea_stock_list():
    df = fdr.StockListing('KRX')
    df = df[['Name', 'Code']]
    df['Display'] = df['Name'] + " (" + df['Code'] + ")"
    return df

krx_df = load_korea_stock_list()
symbols = krx_df['Display'].tolist()
selected = st.selectbox("📌 한국 종목 선택", options=symbols)
manual_symbol = krx_df[krx_df["Display"] == selected]["Code"].values[0]

# -------------------- 날짜 입력 --------------------
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("조회 시작일", value=date.today() - timedelta(days=30))
with col2:
    end_date = st.date_input("조회 종료일", value=date.today())

# -------------------- 한국 주식 조회 --------------------
@st.cache_data(ttl=3600)
def get_korean_stock_data(code, start, end):
    df = fdr.DataReader(code, start, end)
    return df

if st.button("📊 한국 종목 조회"):
    try:
        hist = get_korean_stock_data(manual_symbol, start_date, end_date)
        st.subheader(f"📈 {selected} 주가 차트")
        st.line_chart(hist["Close"])
        st.dataframe(hist.tail(5))
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

# -------------------- 미국 국채 금리 --------------------
st.divider()
st.subheader("💵 미국 국채 금리")

bond_options = {
    "미국 10년물 (^TNX)": "^TNX",
    "미국 30년물 (^TYX)": "^TYX"
}
selected_bond = st.selectbox("미국채 선택", list(bond_options.keys()))

@st.cache_data(ttl=3600)
def get_bond_data(symbol, start, end):
    t = Ticker(symbol)
    df = t.history(start=start, end=end)
    df = df[df.index.get_level_values(0) == symbol]
    df = df.reset_index().set_index("date")
    return df

if st.button("📈 미국채 금리 조회"):
    try:
        symbol = bond_options[selected_bond]
        df = get_bond_data(symbol, start_date, end_date)
        st.line_chart(df["close"])
        st.dataframe(df.tail(5))
    except Exception as e:
        st.error(f"❌ 미국채 데이터 조회 실패: {e}")

# -------------------- 한국 국채 금리 --------------------
st.divider()
st.subheader("📊 한국 국채 금리 (실시간)")

@st.cache_data(ttl=600)
def get_korean_bond_rates():
    url = "https://www.kofiabond.or.kr/proframeWeb/jsp/BDIDX/BDIDX1001.jsp"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table", {"class": "table_style01 type02"})
    data = []
    if table:
        rows = table.find_all("tr")
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) >= 5:
                term = cols[0].text.strip()
                rate = cols[4].text.strip()
                data.append((term, rate))
    return pd.DataFrame(data, columns=["만기", "금리(%)"])

try:
    bond_df = get_korean_bond_rates()
    st.table(bond_df[bond_df["만기"].isin(["1년", "5년", "10년", "20년", "30년"])])
except Exception as e:
    st.error(f"❌ 한국 국채 금리 조회 실패: {e}")
