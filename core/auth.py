import requests]
from core.consts import URL, URL_PERFIL


def login(email, password):
    r = requests.post(
        URL,
        json={"email": email, "password": password},
        headers={"Content-Type": "application/json"},
    )
    if r.status_code != 200:
        return False, None, None

    r = r.json()
    token = r["access"]

    r = requests.get(
        URL_PERFIL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    if "success" in r.json():
        return True, r.json()["user"]["id"], r.json()["user"]["first_name"]
    else:
        return False, None, None

