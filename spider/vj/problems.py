import requests
from sqlalchemy import create_engine, text

from config import SQLALCHEMY_DATABASE_URL
from logger import module_logger

logger = module_logger("poj_solutions")


def main():
    page = 0
    result = []
    while True:
        url = f"https://vjudge.net/problem/data?start={page * 10000}&length=10000&OJId=All&category=all"
        logger.info(f"fetch page {page}")
        resp = requests.get(url).json()
        result.extend(resp["data"])
        if len(resp["data"]) < 10000:
            break
        page += 1

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with engine.connect() as connection:
        source_id = next(
            connection.execute(
                text("select * from sources where name = :name"), {"name": "VJ"}
            )
        ).id
        for item in result:
            title = item["title"]
            problem_id = f"{item['originOJ']} {item['originProb']}"[:32]
            link = f"https://vjudge.net/problem/{item['originOJ']}-{item['originProb']}"

            problem_query = connection.execute(
                text(
                    "select * from problems where source_id = :source_id and problem_id = :problem_id limit 1"
                ),
                {"problem_id": problem_id, "source_id": source_id},
            )
            for problem in problem_query:  # 有此题目，更新
                connection.execute(
                    text(
                        "update problems set  title=:title, link = :link where id = :id"
                    ),
                    {"title": title, "id": problem.id, "link": link},
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
