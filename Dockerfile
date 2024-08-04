FROM python:3.12

WORKDIR /work

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN apt-get update && apt-get install dumb-init && apt-get install -y cron && apt-get -qq clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . .

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
