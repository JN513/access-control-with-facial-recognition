import requests
from core.consts import URL_LOG, TOKEN, SALA


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
