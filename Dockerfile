FROM python:3.10.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /mnt/db /mnt/logs
# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client
# Make the initialization script executable
RUN chmod +x db_init.sh
EXPOSE 8080
# Use the db_init.sh script as entry point
CMD ["./db_init.sh", "gunicorn", "--bind", "0.0.0.0:8080", "app:app"]