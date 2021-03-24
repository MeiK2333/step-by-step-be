import os

from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# 爬虫的配置
SDUT_SPIDER_USER = os.getenv("SDUT_SPIDER_USER")
SDUT_SPIDER_PASS = os.getenv("SDUT_SPIDER_PASS")

SECRET_KEY = os.getenv("SECRET_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
