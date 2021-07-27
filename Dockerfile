FROM alpine
RUN apk add --no-cache sqlite3
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip3

WORKDIR /app

COPY . /app

RUN pip3 --no cache-dir install flask bcrypt mysql.connector urlparse pandas secrets
RUN rc-service mariadb-start


CMD ['python3','init.py']

CMD ['python3','app.py']
