FROM ubuntu:bionic

RUN apt-get update && apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get install -y nodejs git && \
    apt-get -qq clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /app
WORKDIR /app

RUN npm install && \
    npm install -g ts-node typescript

CMD [ "./wait-for-it.sh", "postgres:5432", "--", "ts-node", "src/index.ts" ]
