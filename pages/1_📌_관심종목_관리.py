import streamlit as st
import requests
import FinanceDataReader as fdr

st.set_page_config(page_title="관심 종목 관리", layout="wide")
st.title("📌 관심 종목 관리")

# 1. 전체 종목 목록 가져오기
@st.cache_data
def load_stock_list():
    df_krx = fdr.StockListing("KRX")  # 한국거래소 전체
    df_us = fdr.StockListing("NASDAQ")  # 미국 (선택적)
    combined = df_krx[["Name", "Code"]].copy()
    return combined

stock_df = load_stock_list()

# 2. 검색창
keyword = st.text_input("🔍 관심 종목 이름으로 검색", "삼성전자")
matched = stock_df[stock_df["Name"].str.contains(keyword)]

if not matched.empty:
    selected_row = matched.iloc[0]
    st.markdown(f"**🔎 선택된 종목:** {selected_row['Name']} ({selected_row['Code']})")
    
    if st.button("📥 관심 종목으로 등록"):
        payload = {
            "stock_name": selected_row["Name"],
            "ticker_code": selected_row["Code"] + ".KS"  # yfinance용 형식
        }
        res = requests.post("https://fastapi-backend-io09.onrender.com/add-favorite", json=payload)
        if res.status_code == 200:
            st.success(f"{selected_row['Name']} 종목이 관심 목록에 추가되었습니다.")
        else:
            st.error("등록 실패. 서버 상태를 확인해주세요.")
else:
    st.info("검색 결과가 없습니다.")

# 3. 등록된 관심 종목 조회
st.divider()
st.subheader("📋 등록된 관심 종목 목록")

try:
    favorites = requests.get("https://fastapi-backend-io09.onrender.com/get-favorites").json()
    for fav in favorites:
        st.write(f"✅ {fav['stock_name']} ({fav['ticker_code']})")
except Exception as e:
    st.error(f"📡 서버와 연결 실패: {e}")
