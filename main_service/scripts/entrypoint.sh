#!/bin/bash

source /app/.venv/bin/activate

echo "Waiting for PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started!"

echo "Applying database migrations..."
poetry run alembic -c conf/alembic.ini upgrade head

echo "Starting services..."
exec supervisord -n -c /etc/supervisor/conf.d/supervisord.conf
