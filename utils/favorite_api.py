import requests

def add_favorite_to_db(stock_name, ticker_code):
    url = "https://fastapi-backend-io09.onrender.com/add-favorite"
    data = {
        "stock_name": stock_name,
        "ticker_code": ticker_code
    }
    response = requests.post(url, json=data)
    return response.status_code, response.json()

def get_favorite_stocks():
    url = "https://fastapi-backend-io09.onrender.com/get-favorites"
    response = requests.get(url)
    return response.status_code, response.json()
