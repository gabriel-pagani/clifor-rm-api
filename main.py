import json
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


def main():
    try:
        load_dotenv(override=True)

        api_url = os.getenv("API_URL")
        api_user = os.getenv("API_USER")
        api_user_pwd = os.getenv("API_USER_PWD")

        session = requests.Session()
        session.auth = HTTPBasicAuth(api_user, api_user_pwd)
        session.headers.update({"Accept": "application/json"})

        with open("example.json", "r", encoding="utf-8") as j:
            payload = json.load(j)

        resp = session.post(api_url, json=payload, timeout=30)
        resp.raise_for_status()
    
    except Exception as e:
        print(f"status: {resp.status_code}")
        print(f"error: {e}")


if __name__ == "__main__":
    raise SystemExit(main())
