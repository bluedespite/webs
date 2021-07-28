FROM ubuntu
RUN apt-get update
RUN apt-get install -y python pip sqlite
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./init.py" ]
CMD [ "python", "./app.py" ]
