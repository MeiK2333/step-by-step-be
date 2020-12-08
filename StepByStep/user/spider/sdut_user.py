from typing import Optional

import requests
import time


def sdut_user(username: str) -> Optional[str]:
    # 如果 SDUT 提供的不是 user id，直接返回 GG
    try:
        username = int(username)
    except ValueError:
        return None

    session_url = "https://acm.sdut.edu.cn/onlinejudge3/api/getSession?t=" + str(
        time.time() * 1000
    )
    resp = requests.get(session_url)
    csrf = resp.cookies["csrfToken"]
    url = "https://acm.sdut.edu.cn/onlinejudge3/api/getUserDetail"
    resp = requests.post(
        url,
        json={"userId": username},
        headers={"x-csrf-token": csrf, "cookie": f"csrfToken={csrf}"}
    ).json()
    if resp.get('success') is False:
        return None
    return resp['data']['nickname']
