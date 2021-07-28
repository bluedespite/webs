FROM alpine
RUN apk update
RUN apk add python3 python3-dev  autoconf automake g++ make py3-pip sqlite --no-cache
RUN pip install bcrypt flask
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./init.py" ]
CMD [ "python", "./app.py" ]
