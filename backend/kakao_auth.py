import os
import json
import requests

CLIENT_ID = "48f8318d48bafe040f2d9605f68bf6bb"
token_path = os.path.join(os.getcwd(), "token.json")

def save_tokens(token_json):
    with open(token_path, "w") as f:
        json.dump(token_json, f)

def load_access_token():
    if not os.path.exists(token_path):
        return None
    with open(token_path, "r") as f:
        tokens = json.load(f)
    return tokens.get("access_token")

def refresh_access_token():
    if not os.path.exists(token_path):
        return None
    with open(token_path, "r") as f:
        tokens = json.load(f)
    refresh_token = tokens.get("refresh_token")
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "refresh_token": refresh_token,
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        new_tokens = response.json()
        save_tokens({**tokens, **new_tokens})
        return new_tokens.get("access_token")
    return None
