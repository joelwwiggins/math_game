FROM python:3.10.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /mnt/db /mnt/logs

RUN apt-get update && apt-get install -y postgresql-client iputils-ping netcat-openbsd dnsutils

COPY wait-for-db.sh .
RUN chmod +x wait-for-db.sh

EXPOSE 8080

CMD ["sh", "-c", "./wait-for-db.sh && python init_db.py && gunicorn --config gunicorn.conf.py app:app"]