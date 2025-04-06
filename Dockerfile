FROM python:3.10.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /mnt/db /mnt/logs

# Install PostgreSQL client and network tools
RUN apt-get update && apt-get install -y postgresql-client iputils-ping netcat-openbsd dnsutils

EXPOSE 8080

# Run the init_db.py script then start the Gunicorn server
CMD ["sh", "-c", "python init_db.py && gunicorn --config gunicorn.conf.py app:app"]