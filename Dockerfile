FROM alpine
RUN apk add --no-cache mariadb mariadb-common mariadb-client
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip3
RUN mysqladmin --no-defaults --port=3308 --user=root --protocol=tcp password '12345'
RUN service mysql restart

WORKDIR /app

COPY . /app

RUN pip3 --no cache-dir install flask bcrypt mysql.connector urlparse pandas secrets
RUN rc-service mariadb-start


CMD ['python3','init.py']

CMD ['python3','app.py']
