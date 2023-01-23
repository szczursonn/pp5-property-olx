FROM python:3.11.1-alpine3.17

RUN apk update
RUN apk add gcc python3-dev musl-dev mariadb-dev

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .

EXPOSE 8000

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]