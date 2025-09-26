#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for database to be ready..."
while ! mysqladmin ping -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
    echo "Database is unavailable - sleeping"
    sleep 1
done

echo "Database is ready!"

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Start the application
echo "Starting the application..."
exec "$@"
