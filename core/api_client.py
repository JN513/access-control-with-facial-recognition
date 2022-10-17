import requests
from core.consts import URL_LOG, TOKEN, SALA, DEVICE_CODE, URL_CHECK_TOKEN


def send_ponto(user_id: int):
    data = {"id": user_id, "sala": SALA}

    r = requests.post(
        URL_LOG,
        json=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Token {TOKEN}",
        },
    )

    return r.status_code, r.json()


def get_user_by_token(token: str):
    data = {"token": token, "code": DEVICE_CODE}

    r = requests.post(
        URL_CHECK_TOKEN,
        json=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Token {TOKEN}",
        },
    )

    return r.status_code, r.json()
