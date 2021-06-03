import aiohttp
from bs4 import BeautifulSoup


async def login(username: str, password: str):
    async with aiohttp.ClientSession() as session:
        login_url = "https://codeforces.com/enter?back=%2F"
        # 获取 csrf
        async with session.get(login_url) as resp:
            content = await resp.text()
            soup = BeautifulSoup(content, "html.parser")
            csrf = soup.find(class_="csrf-token").attrs["data-csrf"]
        async with session.post(
            login_url,
            data={
                "csrf_token": csrf,
                "action": "enter",
                "handleOrEmail": username,
                "password": password,
                "_tta": "716",
            },
        ) as resp:
            content = await resp.text()
    return f'var handle = "{username}";' in content
