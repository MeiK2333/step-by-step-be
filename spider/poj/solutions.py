from datetime import datetime

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text

from config import SQLALCHEMY_DATABASE_URL
from logger import module_logger
from schemas.enums import LanguageEnum, ResultEnum

logger = module_logger("poj_solutions")


def to_language_enum(raw_language: str) -> LanguageEnum:
    language = LanguageEnum.Unknown
    raw_language = raw_language.lower()
    if raw_language == "gcc" or raw_language == "c":
        language = LanguageEnum.C
    elif raw_language == "g++" or raw_language == "c++":
        language = language.Cpp
    elif raw_language == "java":
        language = language.Java
    elif raw_language == "pascal":
        language = language.Pascal
    elif raw_language == "fortran":
        language = language.Fortran
    return language


def to_result_enum(raw_result: str) -> ResultEnum:
    result = ResultEnum.Unknown
    if raw_result == "Accepted":
        result = ResultEnum.Accepted
    elif raw_result == "Time Limit Exceeded":
        result = ResultEnum.TimeLimitExceeded
    elif raw_result == "Memory Limit Exceeded":
        result = ResultEnum.MemoryLimitExceeded
    elif raw_result == "Wrong Answer":
        result = ResultEnum.WrongAnswer
    elif raw_result == "Runtime Error":
        result = ResultEnum.RuntimeError
    elif raw_result == "Output Limit Exceeded":
        result = ResultEnum.OutputLimitExceeded
    elif raw_result == "Compile Error":
        result = ResultEnum.CompileError
    elif raw_result == "Presentation Error":
        result = ResultEnum.PresentationError
    elif raw_result == "System Error":
        result = ResultEnum.SystemError
    return result


def to_solution(row: dict) -> dict:
    data = {}
    language = to_language_enum(row["language"])
    if language == LanguageEnum.Unknown:
        logger.warning(f"Unknown language! row = {row}")
    result = to_result_enum(row["result"])
    if result == ResultEnum.Unknown:
        logger.warning(f"Unknown result! row = {row}")

    data["result"] = result.name
    data["language"] = language.name
    data["time_used"] = int(row["time"][:-2]) if row["time"] else 0
    data["memory_used"] = int(row["memory"][:-1]) if row["memory"] else 0
    data["code_len"] = int(row["codeLength"][:-1])
    data["username"] = row["user"]
    data["nickname"] = row["user"]
    data["submitted_at"] = datetime.strptime(row["sub_time"], "%Y-%m-%d %H:%M:%S")
    return data


def get_solution(username: str, last_spider: int):
    result = []
    while True:
        url = f"http://poj.org/status?user_id={username}&bottom={last_spider}"
        logger.info(f"crawl {username}, start = {last_spider}")
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "html.parser")
        table = soup.find_all("table")[4]
        trs = table.find_all("tr")
        for tr in trs[1:][::-1]:
            tds = tr.find_all("td")
            item = {
                "run_id": tds[0].text,
                "user": tds[1].text,
                "problem": tds[2].text,
                "result": tds[3].text,
                "memory": tds[4].text,
                "time": tds[5].text,
                "language": tds[6].text,
                "codeLength": tds[7].text,
                "sub_time": tds[8].text,
            }
            result.append(item)
            last_spider = max(int(item["run_id"]), last_spider)
        if len(trs) < 21:
            break
    return result


def main():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with engine.connect() as connection:
        bind_users = connection.execute(
            text(
                "select *, bind_user.id as bid from bind_user "
                "left join sources s "
                "on s.id = bind_user.source_id "
                "where s.name = 'POJ'"
            )
        )
        for bind_user in bind_users:
            last_spider = bind_user.last_spider
            rows = get_solution(bind_user.username, last_spider)
            logger.info(f"crawl solutions {len(rows)} rows")
            for row in rows:
                param = to_solution(row)

                param["source_id"] = bind_user.source_id
                param["bind_user_id"] = bind_user.bid
                problem_id = connection.execute(
                    text(
                        "select id from problems "
                        "where source_id = :source_id and problem_id = :problem_id"
                    ),
                    {"problem_id": row["problem"], "source_id": bind_user.source_id},
                )
                try:
                    param["problem_id"] = next(problem_id).id
                except StopIteration:  # 如果该提交所对应的题目不存在，则跳过该提交
                    logger.warning(f"无对应题目：row = {row}!!!")
                    continue
                connection.execute(
                    text(
                        "insert into solutions "
                        "(username, nickname, result, time_used, memory_used, "
                        "code_len, language, submitted_at, bind_user_id, problem_id, source_id) "
                        "values "
                        "(:username, :nickname, :result, :time_used, :memory_used, "
                        ":code_len, :language, :submitted_at, :bind_user_id, :problem_id, :source_id)"
                    ),
                    param,
                )
                last_spider = max(int(row["run_id"]), last_spider)


if __name__ == "__main__":
    main()
