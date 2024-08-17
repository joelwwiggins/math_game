FROM python:3.10.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /mnt/db

EXPOSE 8080


CMD ["python", "init_db.py", "&&", "gunicorn", "app:app"]