import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text

from config import SQLALCHEMY_DATABASE_URL
from logger import module_logger

logger = module_logger("poj_problems")


def get_pages():
    resp = requests.get("http://poj.org/problemlist")
    soup = BeautifulSoup(resp.content, "html.parser")
    center = soup.find("center")
    a = center.find_all("a")[-1]
    return int(a.text)


def fetch(page: int):
    resp = requests.get(f"http://poj.org/problemlist?volume={page}")
    soup = BeautifulSoup(resp.content, "html.parser")
    table = soup.find_all("table")[4]
    trs = table.find_all("tr")
    result = []
    for tr in trs[1:]:
        td = tr.find("td")
        problem_id = td.text.strip()
        a = tr.find("a")
        href = "http://poj.org/" + a.attrs["href"]
        title = a.text.strip()
        result.append({"link": href, "title": title, "problem_id": problem_id})
    return result


def main():
    pages = get_pages()
    result = []
    for i in range(pages):
        page = i + 1
        logger.info(f"fetch page {page}")
        result.extend(fetch(page))

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with engine.connect() as connection:
        source_id = next(
            connection.execute(
                text("select * from sources where name = :name"), {"name": "POJ"}
            )
        ).id
        for item in result:
            problem_id = item["problem_id"]
            title = item["title"]
            link = item["link"]

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
                    {"id": problem.id, "title": title, "link": link},
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
                        "source_id": source_id,
                        "problem_id": problem_id,
                        "title": title,
                        "link": link,
                    },
                )
                logger.info(f"insert problem {problem_id} - {title}")


if __name__ == "__main__":
    main()
