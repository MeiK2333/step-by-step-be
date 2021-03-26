import time

import requests
from sqlalchemy import create_engine, text

from config import SQLALCHEMY_DATABASE_URL
from logger import module_logger

logger = module_logger("sdut_problems")


def get_csrf(session: requests.Session):
    session_url = "https://acm.sdut.edu.cn/onlinejudge3/api/getSession?t=" + str(
        time.time() * 1000
    )
    resp = session.get(session_url)
    csrf = resp.cookies["csrfToken"]
    return csrf


def main():
    session = requests.Session()
    csrf = get_csrf(session)
    session.headers.update({"x-csrf-token": csrf})
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    url = "https://acm.sdut.edu.cn/onlinejudge3/api/getProblemList"
    page = 1
    result = []
    while True:
        data = {"limit": 20, "page": page}
        logger.info(f"get page {page}")
        resp = session.post(url, json=data).json()
        result.extend(resp["data"]["rows"])
        if len(resp["data"]["rows"]) < 20:
            break
        page += 1

    with engine.connect() as connection:
        source_id = next(
            connection.execute(
                text("select * from sources where name = :name"), {"name": "SDUT"}
            )
        ).id
        for item in result:
            problem_id = str(item["problemId"])
            title = item["title"]
            link = f"https://acm.sdut.edu.cn/onlinejudge3/problems/{problem_id}"

            problem_query = connection.execute(
                text(
                    "select * from problems where source_id = :source_id and problem_id = :problem_id limit 1"
                ),
                {"source_id": source_id, "problem_id": problem_id},
            )
            for problem in problem_query:  # 有此题目，更新
                connection.execute(
                    text(
                        "update problems set  title=:title, link = :link where id = :id"
                    ),
                    {"title": title, "link": link, "id": problem.id},
                )
                logger.info(f"update problem {problem_id} - {title}")
                break
            else:  # 无此题目，插入
                connection.execute(
                    text(
                        "insert into problems "
                        "(problem_id, source_id, title, link) "
                        "values "
                        "(:problem_id, :source_id, :title, :link)"
                    ),
                    {
                        "problem_id": problem_id,
                        "title": title,
                        "link": link,
                        "source_id": source_id,
                    },
                )
                logger.info(f"insert problem {problem_id} - {title}")


if __name__ == "__main__":
    main()
