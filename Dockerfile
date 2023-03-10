FROM python:3.9.14-alpine3.16

WORKDIR /app

RUN apk update && apk add gcc musl-dev build-base postgresql-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY locales locales
COPY notprovide notprovide
COPY src src

CMD ["python", "-u", "src/main.py"]
