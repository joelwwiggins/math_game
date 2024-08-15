FROM python:3.10.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 8080

# Define environment variable
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080


CMD ["python", "app.py"]
