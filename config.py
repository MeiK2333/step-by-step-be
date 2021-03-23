import os

from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# 爬虫的配置
SDUT_SPIDER_USER = os.getenv("SDUT_SPIDER_USER")
SDUT_SPIDER_PASS = os.getenv("SDUT_SPIDER_PASS")
