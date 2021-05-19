import time

import aiohttp


async def login(username: str, password: str):
    async with aiohttp.ClientSession() as session:
        session_url = "https://acm.sdut.edu.cn/onlinejudge3/api/getSession?t=" + str(
            time.time() * 1000
        )
        async with session.get(session_url) as resp:
            csrf = resp.cookies.get("csrfToken").value
        session.headers.update({"x-csrf-token": csrf})
        login_url = "https://acm.sdut.edu.cn/onlinejudge3/api/login"
        async with session.post(
            login_url, json={"loginName": username, "password": password}
        ) as resp:
            content = await resp.json()
    return content
