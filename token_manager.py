import os
from pathlib import Path

import requests
from dotenv import load_dotenv, set_key

ENV_PATH = Path(__file__).parent / ".env"
TOKEN_URL = "https://id.twitch.tv/oauth2/token"
VALIDATE_URL = "https://id.twitch.tv/oauth2/validate"
TOKEN_VAR = "ACCESS_TOKEN"


def is_token_valid(token):
    if not token:
        return False
    response = requests.get(
        VALIDATE_URL,
        headers={"Authorization": f"OAuth {token}"},
        timeout=10,
    )
    return response.status_code == 200


def generate_token():
    response = requests.post(
        TOKEN_URL,
        params={
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
            "grant_type": "client_credentials",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def save_token(token):
    set_key(str(ENV_PATH), TOKEN_VAR, token)
    os.environ[TOKEN_VAR] = token


def ensure_token():
    load_dotenv(ENV_PATH)
    token = os.getenv(TOKEN_VAR)

    if not is_token_valid(token):
        token = generate_token()
        save_token(token)

    return token