FROM python:3.10.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

# Ensure the /mnt/db and /mnt/logs directories exist
RUN mkdir -p /mnt/db /mnt/logs

CMD ["python", "app.py"]