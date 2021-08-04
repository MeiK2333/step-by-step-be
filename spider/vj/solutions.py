from datetime import datetime

import requests
from sqlalchemy import create_engine, text

from logger import module_logger
from config import VJ_SPIDER_PASS, VJ_SPIDER_USER, SQLALCHEMY_DATABASE_URL
from schemas.enums import ResultEnum, LanguageEnum

logger = module_logger("vj_solutions")


def login():
    form = {"username": VJ_SPIDER_USER, "password": VJ_SPIDER_PASS}
    resp = requests.post("https://vjudge.net/user/login", data=form)
    return resp.cookies


def vj_item_to_solution(user: str, item: dict) -> dict:
    data = {
        "problem": item[0] + " " + item[1],
        "time_used": item[2],
        "memory_used": item[3],
        "code_len": item[4],
        "username": user,
        "nickname": user,
        # 返回数据中没有语言信息
        "language": LanguageEnum.Unknown.name,
    }
    # 如果没有 AC 时间，则说明这个题目还没通过
    if item[5] is None:
        # 只知道没 AC，但不知道具体是什么结果
        data["result"] = ResultEnum.Unknown.name
        data["submitted_at"] = datetime.fromtimestamp(item[6])
    else:
        data["result"] = ResultEnum.Accepted.name
        data["submitted_at"] = datetime.fromtimestamp(item[5])
    return data


def main():
    logger.info("start")
    cookies = login()
    logger.info("logged")
    fetched_user = set()
    bind_user_to_id = {}
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with engine.connect() as connection:
        source_id = next(
            connection.execute(
                text("select * from sources where name = :name"), {"name": "VJ"}
            )
        ).id

        bind_users = connection.execute(
            text(
                "select *, bind_user.id as bid from bind_user "
                "left join sources s "
                "on s.id = bind_user.source_id "
                "where s.name = 'VJ'"
            )
        )
        for bind_user in bind_users:
            username = bind_user.username
            bid = bind_user.bid
            bind_user_to_id[username] = bid

        # 根据 group 获取，获取一天内有过登录的所有账号AC数据
        url = "https://vjudge.net/group/solveEntries/sdutsbs?queryWindowMillis=7200000"
        # 重试三次，因为 VJ 的接口可能超时
        # 第一次超时，后续请求有可能命中缓存而成功
        for i in range(3):
            try:
                resp = requests.get(url, cookies=cookies).json()
            except Exception as ex:
                logger.exception(ex)
            else:
                break
        else:
            logger.error('请求失败')
            return

        for user, items in resp.items():
            fetched_user.add(user)
            if user not in bind_user_to_id.keys():
                logger.warning(f"{user} 没有关联的账号")
                continue
            logger.info(f"更新 {user} 的提交数据")

            # 注意 VJ 接口返回的数据为全量数据（虽然有部分信息丢失），所以在更新时需要清除对应用户所有历史数据
            for item in items:
                param = vj_item_to_solution(user, item)
                problem_id = connection.execute(
                    text(
                        "select id from problems "
                        "where source_id = :source_id and problem_id = :problem_id"
                    ),
                    {"source_id": source_id, "problem_id": param["problem"]},
                )
                try:
                    problem_id = next(problem_id).id
                except StopIteration:  # 如果该提交所对应的题目不存在，则跳过该提交
                    logger.warning(f"无对应题目：row = {item}!!!")
                    continue
                param["bind_user_id"] = bind_user_to_id[user]
                param["source_id"] = source_id
                param["problem_id"] = problem_id
                solutions = connection.execute(
                    text(
                        "select * from solutions where bind_user_id = :bid and problem_id = :problem_id"
                    ),
                    {"bid": bind_user_to_id[user], "problem_id": problem_id},
                )
                for solution in solutions:
                    param["id"] = solution.id
                    # 已有该用户该题目的提交，更新
                    connection.execute(
                        text(
                            "update solutions set "
                            "username = :username, nickname = :nickname, result = :result, time_used = :time_used, "
                            "memory_used = :memory_used, code_len = :code_len, language = :language, "
                            "submitted_at = :submitted_at "
                            "where id = :id"
                        ),
                        param,
                    )
                    break  # 这里的 break 是为了不触发后面的 else
                else:
                    # 没有该用户的提交，插入
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


if __name__ == "__main__":
    main()
