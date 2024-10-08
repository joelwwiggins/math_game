FROM python:3.10.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /mnt/db
# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client
EXPOSE 8080
CMD ["sh", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:8080 app:app"]