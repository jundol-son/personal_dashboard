import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="뉴스 요약", layout="wide")
st.title("📰 뉴스 요약")

keyword = st.text_input("🔍 검색할 키워드 입력", "삼성전자")

if st.button("뉴스 검색"):
    search_url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
    response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(response.text, "html.parser")
    news_items = soup.select(".news_area")[:5]  # 상위 5개만 출력

    if not news_items:
        st.warning("뉴스 결과가 없습니다.")
    else:
        for item in news_items:
            title = item.select_one(".news_tit").text
            link = item.select_one(".news_tit")["href"]
            press = item.select_one(".info_group a").text

            st.markdown(f"**[{title}]({link})**")
            st.caption(f"📰 {press}")
            st.markdown("---")
