from typing import Optional

import requests
from bs4 import BeautifulSoup


def poj_user(username: str) -> Optional[str]:
    url = f'http://poj.org/userstatus?user_id={username}'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    font = soup.find('font')
    if 'Error Occurred' in font.text:
        return None
    font = soup.find('center').find('font').text
    nickname = font[len(username) + 2:]
    return nickname
