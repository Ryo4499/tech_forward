FROM python:3.9-alpine

RUN apk add --no-cache mariadb-connector-c-dev gcc musl-dev
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN addgroup -S app && adduser -S -G app app && chown -R app:app /app
USER app
