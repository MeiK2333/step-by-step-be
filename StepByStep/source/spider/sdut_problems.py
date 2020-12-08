import time

import requests
from source.models import Problem, Source


def sdut_problems():
    session_url = "https://acm.sdut.edu.cn/onlinejudge3/api/getSession?t=" + str(
        time.time() * 1000
    )
    resp = requests.get(session_url)
    csrf = resp.cookies["csrfToken"]
    url = "https://acm.sdut.edu.cn/onlinejudge3/api/getProblemList"
    page = 1
    result = []
    while True:
        data = {"limit": 20, "page": page}
        print(f"get page {page}")
        resp = requests.post(
            url,
            json=data,
            headers={"x-csrf-token": csrf, "cookie": f"csrfToken={csrf}"},
        ).json()
        result.extend(resp["data"]["rows"])
        if len(resp["data"]["rows"]) < 20:
            break
        page += 1

    source, _ = Source.objects.get_or_create(name="sdut")
    for item in result:
        problem_id = str(item["problemId"])
        title = item["title"]
        link = f"https://acm.sdut.edu.cn/onlinejudge3/problems/{problem_id}"
        Problem.objects.update_or_create(
            source=source,
            problem_id=problem_id,
            defaults={"title": title, "link": link},
        )
