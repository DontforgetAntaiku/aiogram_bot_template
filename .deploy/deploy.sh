#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
else
    echo ".env file not found!"
    exit 1
fi

echo "Starting deployment for $WEBHOOK_BASE_URL..."

# 1. Create necessary directories
mkdir -p ./.deploy/nginx/certbot/conf
mkdir -p ./.deploy/nginx/certbot/www

# 2. Start Nginx first (will serve challenge on port 80)
docker compose up -d nginx

# 3. Check if certificate already exists
if [ ! -d "./.deploy/nginx/certbot/conf/live/$WEBHOOK_BASE_URL" ]; then
    echo "Requesting SSL certificate..."
    docker compose run --rm certbot certonly --webroot \
        --webroot-path=/var/www/certbot \
        --register-unsafely-without-email \
        --agree-tos --no-eff-email \
        -d $WEBHOOK_BASE_URL
else
    echo "Certificate already exists."
fi

# 4. Start everything else
echo "Restarting services..."
docker compose up -d

echo "System is up and running!"
