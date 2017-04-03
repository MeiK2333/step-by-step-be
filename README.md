# StepByStep
已经不知道是第几版的StepByStep

# 开发环境
Python 2.7

Django 1.8.7

MongoDB 2.6.10

SQLite3

# 所需依赖
## python包
xlrd

pymongo

bs4

requests

uwsgi

# 配置
## 数据库配置
控制台CD到项目根目录，执行
**python manage.py makemigrations**、
**python manage.py migrate**
以初始化数据库，之后执行
**python manage.py createsuperuser**
来创建超级管理员。
Mongo数据库名为StepByStepData，不需要额外配置。

## uwsgi配置
在项目根目录下新建**uwsgi.ini**配置文件，内容为
```ini
[uwsgi]

# Django-related settings

socket = :8088

# the base directory (full path)
chdir           = {{ 项目路径 }}

# Django s wsgi file
module          = StepByStep.wsgi

# process-related settings
# master
master          = true

# maximum number of worker processes
processes       = 4

# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true
```

配置中的socket可以不为8088,但必须与nginx中的端口一致

## nginx配置
新建配置文件，内容为
```
server {
    listen 80;
    server_name {{ 解析域名 }};
    location / {
        include /etc/nginx/uwsgi_params;
        uwsgi_pass 127.0.0.1:8088;
    }
    location /static {
        expires 30d;
        autoindex on;
        add_header Cache-Control private;
        alias {{ 静态文件目录 }};
    }
}
```

# 启动命令
```shell
cd {{ 项目目录 }}
uwsgi -d --ini uwsgi.ini
sudo service nginx restart
```