import time
from datetime import datetime, timedelta

import requests
from sqlalchemy import create_engine
from sqlalchemy import text

from config import SDUT_SPIDER_USER, SDUT_SPIDER_PASS, SQLALCHEMY_DATABASE_URL
from logger import module_logger
from schemas.enums import ResultEnum, LanguageEnum

logger = module_logger("sdut_solutions")


def get_csrf(session: requests.Session):
    session_url = "https://acm.sdut.edu.cn/onlinejudge3/api/getSession?t=" + str(
        time.time() * 1000
    )
    resp = session.get(session_url)
    csrf = resp.cookies["csrfToken"]
    return csrf


def login(username: str, password: str):
    session = requests.Session()
    csrf = get_csrf(session)
    session.headers.update({"x-csrf-token": csrf})
    login_url = "https://acm.sdut.edu.cn/onlinejudge3/api/login"
    session.post(login_url, json={"loginName": username, "password": password})
    return session


def get_userid_by_username(username: str, session: requests.Session) -> int:
    url = "https://acm.sdut.edu.cn/onlinejudge3/api/getUserList"
    data = {
        "username": username,
        "page": 1,
        "order": [["accepted", "DESC"]],
        "limit": 20,
    }

    resp = session.post(url, json=data)
    for row in resp.json()["data"]["rows"]:
        if row["username"].lower() == username.lower():
            return row["userId"]
    return -1


def get_solution(user_id: int, start: int, session: requests.Session):
    url = "https://acm.sdut.edu.cn/onlinejudge3/api/getSolutionList"
    result = []
    while True:
        logger.info(f"crawl {user_id}, start = {start}")
        data = {
            "gt": start,
            "limit": 1000,
            "order": [["solutionId", "DESC"]],
            "userId": user_id,
        }
        resp = session.post(url, json=data)
        rows = resp.json()["data"]["rows"][::-1]
        if len(rows) == 0:
            break
        for row in rows:
            res = to_result_enum(row["result"])
            if res == ResultEnum.Unknown:  # 如果遇到未知的数据，直接中断，剩下的下次爬取再说
                logger.warning(f"crawl result {res}, break!")
                return result
            result.append(row)
            start = max(row["solutionId"], start)
    return result


def to_language_enum(raw_language: str) -> LanguageEnum:
    language = LanguageEnum.Unknown
    raw_language = raw_language.lower()
    if raw_language == "gcc" or raw_language == "c":
        language = LanguageEnum.C
    elif raw_language == "g++" or raw_language == "c++":
        language = language.Cpp
    elif (
        raw_language == "python2"
        or raw_language == "python3"
        or raw_language == "python"
    ):
        language = language.Python
    elif raw_language == "go":
        language = language.Go
    elif raw_language == "rust":
        language = language.Rust
    elif raw_language == "javascript":
        language = language.JavaScript
    elif raw_language == "java":
        language = language.Java
    elif raw_language == "typescript":
        language = language.TypeScript
    elif raw_language == 'c#':
        language = language.CSharp
    return language


def to_result_enum(raw_result: int) -> ResultEnum:
    result = ResultEnum.Unknown
    if raw_result == 1:
        result = ResultEnum.Accepted
    elif raw_result == 2:
        result = ResultEnum.TimeLimitExceeded
    elif raw_result == 3:
        result = ResultEnum.MemoryLimitExceeded
    elif raw_result == 4:
        result = ResultEnum.WrongAnswer
    elif raw_result == 5:
        result = ResultEnum.RuntimeError
    elif raw_result == 6:
        result = ResultEnum.OutputLimitExceeded
    elif raw_result == 7:
        result = ResultEnum.CompileError
    elif raw_result == 8:
        result = ResultEnum.PresentationError
    elif raw_result == 11:
        result = ResultEnum.SystemError
    return result


def to_solution(row: dict) -> dict:
    data = {}
    result = to_result_enum(row["result"])
    if result == ResultEnum.Unknown:
        logger.warning(f"Unknown result! row = {row}")
    language = to_language_enum(row["language"])
    if language == LanguageEnum.Unknown:
        logger.warning(f"Unknown language! row = {row}")

    data["result"] = result.name
    data["language"] = language.name
    data["time_used"] = row["time"]
    data["memory_used"] = row["memory"]
    data["code_len"] = row["codeLength"]
    data["username"] = row["user"]["username"]
    data["nickname"] = row["user"]["nickname"]
    # 时区转换，python datetime 并不完全符合 ISO 标准，因此手动偏移时区
    data["submitted_at"] = datetime.strptime(
        row["createdAt"], "%Y-%m-%dT%H:%M:%S.000Z"
    ) + timedelta(hours=8)
    return data


def main():
    session = login(SDUT_SPIDER_USER, SDUT_SPIDER_PASS)
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with engine.connect() as connection:
        bind_users = connection.execute(
            text(
                "select *, bind_user.id as bid from bind_user "
                "left join sources s "
                "on s.id = bind_user.source_id "
                "where s.name = 'SDUT'"
            )
        )
        for bind_user in bind_users:
            last_spider = bind_user.last_spider
            logger.info(f"crawl {bind_user.username}")
            try:
                user_id = get_userid_by_username(bind_user.username, session)
                logger.info(f"user_id = {user_id}")
                rows = get_solution(user_id, last_spider, session)
                logger.info(f"crawl solutions {len(rows)} rows")
                for row in rows:
                    param = to_solution(row)
                    param["id"] = None
                    param["bind_user_id"] = bind_user.bid
                    param["source_id"] = bind_user.source_id
                    problem_id = connection.execute(
                        text(
                            "select id from problems "
                            "where source_id = :source_id and problem_id = :problem_id"
                        ),
                        {
                            "source_id": bind_user.source_id,
                            "problem_id": str(row["problem"]["problemId"]),
                        },
                    )
                    try:
                        param["problem_id"] = next(problem_id).id
                    except StopIteration:  # 如果该提交所对应的题目不存在，则跳过该提交
                        logger.warning(f"无对应题目：row = {row}!!!")
                        continue
                    connection.execute(
                        text(
                            "insert into solutions "
                            "(id, username, nickname, result, time_used, memory_used, "
                            "code_len, language, submitted_at, bind_user_id, problem_id, source_id) "
                            "values "
                            "(:id, :username, :nickname, :result, :time_used, :memory_used, "
                            ":code_len, :language, :submitted_at, :bind_user_id, :problem_id, :source_id)"
                        ),
                        param,
                    )
                    last_spider = max(row["solutionId"], last_spider)
            except KeyboardInterrupt:
                logger.info("ctrl - c, break")
                break
            except Exception as ex:
                logger.warning(repr(ex))
            finally:
                connection.execute(
                    text(
                        "update bind_user set last_spider = :last_spider "
                        "where username = :username and source_id = :source_id"
                    ),
                    {
                        "last_spider": last_spider,
                        "username": bind_user.username,
                        "source_id": bind_user.source_id,
                    },
                )


if __name__ == "__main__":
    main()
