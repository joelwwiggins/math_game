#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
# Wait for PostgreSQL to be ready with increased timeout
max_attempts=30
counter=0
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" || [ $counter -eq $max_attempts ]; do
  echo "PostgreSQL is unavailable - sleeping"
  counter=$((counter+1))
  sleep 5
done

if [ $counter -eq $max_attempts ]; then
  echo "Failed to connect to PostgreSQL after $max_attempts attempts"
  exit 1
fi

echo "PostgreSQL is up - initializing database"
python init_db.py

echo "Database initialization complete - starting application"
exec "$@"
