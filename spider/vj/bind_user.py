import aiohttp


async def login(username: str, password: str):
    async with aiohttp.ClientSession() as session:
        login_url = "https://vjudge.net/user/login"
        async with session.post(
            login_url, data={"username": username, "password": password}
        ) as resp:
            content = await resp.text()
    return content == "success"
