from schemas.auth import get_password_hash
from sqlalchemy import create_engine, text

from config import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def create_superuser():
    with engine.connect() as connection:
        user_count = connection.execute("select count(1) as cnt from users")
        if next(user_count).cnt > 0:
            return

        username = input("username: ")
        password = input("password: ")
        connection.execute(
            text(
                "insert into users (username, hashed_password, robot) values (:username, :hashed_password, :robot)"
            ),
            {
                "username": username,
                "hashed_password": get_password_hash(password),
                "robot": False,
            },
        )
        connection.execute(
            text("insert into roles (id, name, user_id) values (:id, :name, :user_id)"),
            {"id": 1, "name": "admin", "user_id": 1},
        )


def create_sources():
    with engine.connect() as connection:
        connection.execute(
            text("insert into sources (id, name, link) values (:id, :name, :link)"),
            {"id": 1, "name": "SDUT", "link": "https://acm.sdut.edu.cn/onlinejudge3/"},
        )
        connection.execute(
            text("insert into sources (id, name, link) values (:id, :name, :link)"),
            {"id": 2, "name": "POJ", "link": "http://poj.org/"},
        )
        connection.execute(
            text("insert into sources (id, name, link) values (:id, :name, :link)"),
            {"id": 3, "name": "VJ", "link": "https://vjudge.net/"},
        )
        connection.execute(
            text("insert into sources (id, name, link) values (:id, :name, :link)"),
            {"id": 4, "name": "CF", "link": "https://codeforces.com/"},
        )


def install():
    create_superuser()
    create_sources()


if __name__ == "__main__":
    install()
