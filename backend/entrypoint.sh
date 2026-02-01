#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
echo "HOST: $DB_HOST"
echo "PORT: $DB_PORT"
echo "USER: $DB_USER"

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "PostgreSQL not ready - retrying..."
  sleep 2
done

echo "PostgreSQL is up and accepting connections"

echo "Running makemigrations..."
python manage.py makemigrations --noinput

echo "Running migrate..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if not exists..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(username="admin", password="password", email="admin@example.com")
    print("Superuser created")
else:
    print("Superuser already exists")
EOF

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000