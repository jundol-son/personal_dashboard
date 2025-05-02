import requests
from datetime import datetime

URLS = [
    "https://fastapi-backend-io09.onrender.com",     # FastAPI
    "https://streamlit-dashboard-wlrq.onrender.com"        # Streamlit (필요 시)
]

for url in URLS:
    try:
        r = requests.get(url)
        print(f"{datetime.now()} ✅ Ping {url} 성공 - {r.status_code}")
    except Exception as e:
        print(f"{datetime.now()} ❌ Ping {url} 실패 - {e}")
