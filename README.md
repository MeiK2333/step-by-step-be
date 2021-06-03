# StepByStep

## install

修改 alembic.ini 中数据库连接参数

```shell
pip install -r requirements.txt
alembic upgrade head
python install.py
```

## migrate

```shell
alembic upgrade head
```

## run

```shell
uvicorn main:app
```

## TODO

- 用户管理
