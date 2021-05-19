import aiohttp


async def login(username: str, password: str):
    async with aiohttp.ClientSession() as session:
        login_url = "http://poj.org/login"
        async with session.post(
            login_url,
            data={
                "user_id1": username,
                "password1": password,
                "B1": "login",
                "url": "%2F",
            },
        ) as resp:
            content = await resp.text()
    return not (
        "<input type=text name=user_id1 size=10 style='font-family:monospace'>"
        in content
    )
