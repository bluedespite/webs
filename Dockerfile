FROM alpine
RUN apk update
RUN apk add python3 python3-dev  autoconf automake g++ make py3-pip sqlite --no-cache
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./app.py" ]
