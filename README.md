# 依赖
- python2.7
- Flask
- flask_login
- flask_wtf
- flask_mongoengine
- pymongo
- MongoDB

# 还未完成的功能
- 前端（我写的很差）
- 个人页面（所有的数据都有，但是要写匹配的前端）
- 前端、前端、还有前端

# 使用
- 按照自己的配置修改config.py
- 将spriders中的除base之外的爬虫设置为定时任务
- python run.py(Debug模式) or 使用uwsgi或者其他方式发布

# 扩展平台支持
- 在config.py中添加要支持的平台
- 在spriders文件夹中添加对应平台的爬虫
- 扩展爬虫可以参照已有的两个爬虫，当然也可以完全自己写
- 将爬虫设置为定时任务
- 完成
