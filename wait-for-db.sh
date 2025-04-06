#!/bin/bash
set -e

host="${POSTGRES_HOST:-mathgame-db}"
port="${POSTGRES_PORT:-5432}"
max_attempts=30
attempt=1

echo "Waiting for $host:$port to be ready..."

while [ $attempt -le $max_attempts ]; do
  if nc -z -v "$host" "$port" 2>&1 | tee /dev/stderr; then
    echo "Database is ready!"
    exit 0
  fi
  echo "Attempt $attempt/$max_attempts: Database not ready, retrying in 5 seconds..."
  sleep 5
  ((attempt++))
done

echo "Failed to connect to $host:$port after $max_attempts attempts"
exit 1