import streamlit as st
import requests
import FinanceDataReader as fdr
from yahooquery import Ticker
from datetime import date, timedelta

st.set_page_config(page_title="관심 종목 관리", layout="wide")
st.title("📌 관심 종목 관리 및 주가 조회")

FASTAPI_URL = "https://fastapi-backend-io09.onrender.com"  # ← 본인 주소로 교체

# 종목 리스트 캐시
@st.cache_data
def load_krx():
    df = fdr.StockListing("KRX")[["Name", "Code"]]
    return df

krx_df = load_krx()

# 🔍 종목 검색
keyword = st.text_input("🔍 종목명으로 검색", "삼성전자")
matched = krx_df[krx_df["Name"].str.contains(keyword)]

if not matched.empty:
    selected = matched.iloc[0]
    st.markdown(f"**🔎 선택:** {selected['Name']} ({selected['Code']})")

    if st.button("📥 관심 종목 등록"):
        payload = {
            "stock_name": selected["Name"],
            "ticker_code": selected["Code"]  # yahooquery가 자동 처리
        }
        res = requests.post(f"{FASTAPI_URL}/add-favorite", json=payload)
        if res.status_code == 200:
            st.success(f"{selected['Name']} 등록 완료 ✅")
        else:
            st.error("등록 실패 😢")
else:
    st.info("검색 결과가 없습니다.")

st.divider()
st.subheader("✅ 관심 종목 목록")

# 관심 종목 조회 + 주가 표시
try:
    favorites = requests.get(f"{FASTAPI_URL}/get-favorites").json()
    if favorites:
        selected_stock = st.selectbox("📌 선택 종목", [f"{f['stock_name']} ({f['ticker_code']})" for f in favorites])
        selected_ticker = next(f["ticker_code"] for f in favorites if f["stock_name"] in selected_stock)

        # yahooquery로 주가 조회
        ticker = Ticker(selected_ticker)
        st.markdown(f"### 📊 {selected_stock} 주가 정보")
        df = ticker.history(start=date.today() - timedelta(days=30), end=date.today())
        st.line_chart(df["close"])

        info = ticker.summary_detail.get(selected_ticker, {})
        st.write(f"📈 현재가: {info.get('regularMarketPrice', 'N/A')}원")
        st.write(f"💰 시가총액: {info.get('marketCap', 'N/A')}")
        st.write(f"📊 배당 수익률: {round(info.get('dividendYield', 0) * 100, 2)}%")
    else:
        st.info("등록된 관심 종목이 없습니다.")
except Exception as e:
    st.error(f"📡 서버 오류 또는 데이터 조회 실패: {e}")
