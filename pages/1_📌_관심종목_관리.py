import streamlit as st
import requests
import pandas as pd
from datetime import date

st.set_page_config(page_title="📊 KRX & 금리 대시보드", layout="wide")
st.title("📊 한국은행 Open API 기반 - 경제 지표 대시보드")

API_KEY = st.secrets["BOK_API_KEY"]  # 🔐 secrets.toml 또는 .env
base_url = "https://ecos.bok.or.kr/api"

today = date.today().strftime("%Y%m%d")

# 공통 API 요청 함수
def fetch_bok_api(url):
    try:
        res = requests.get(url)
        data = res.json()
        rows = data.get("StatisticSearch", {}).get("row", [])
        return pd.DataFrame(rows)
    except Exception as e:
        st.error(f"❌ API 요청 실패: {e}")
        return pd.DataFrame()

# 주요 환율 (통계코드: 731Y001)
st.subheader("💱 주요국 환율")
url_fx = f"{base_url}/StatisticSearch/{API_KEY}/json/kr/1/20/731Y001/D/{today}/{today}/0000001,0000002,0000003"
df_fx = fetch_bok_api(url_fx)
if not df_fx.empty:
    df_fx = df_fx[["ITEM_NAME1", "DATA_VALUE"]]
    df_fx.columns = ["통화", "환율 (원)"]
    st.table(df_fx)

# KOSPI / KOSDAQ (통계코드: 802Y001)
st.subheader("📈 KOSPI / KOSDAQ")
url_idx = f"{base_url}/StatisticSearch/{API_KEY}/json/kr/1/20/802Y001/D/{today}/{today}/0000001,0000002"
df_idx = fetch_bok_api(url_idx)
if not df_idx.empty:
    df_idx = df_idx[["ITEM_NAME1", "DATA_VALUE"]]
    df_idx.columns = ["지수", "종가"]
    st.table(df_idx)

# 국고채 금리 (통계코드: 722Y001)
st.subheader("💵 국고채 금리")
bond_codes = {
    "국고채 1년": "0101001",
    "국고채 3년": "0101003",
    "국고채 5년": "0101005",
    "국고채 10년": "0101010",
}
bond_items = ",".join(bond_codes.values())
url_bond = f"{base_url}/StatisticSearch/{API_KEY}/json/kr/1/10/722Y001/D/{today}/{today}/{bond_items}"
df_bond = fetch_bok_api(url_bond)
if not df_bond.empty:
    df_bond["만기"] = df_bond["ITEM_NAME1"].map({v: k for k, v in bond_codes.items()})
    df_bond = df_bond[["만기", "DATA_VALUE"]]
    df_bond.columns = ["만기", "금리 (%)"]
    st.table(df_bond)
