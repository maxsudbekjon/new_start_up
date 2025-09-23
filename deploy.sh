#!/bin/bash
cd /var/www/myproject
git pull origin main
docker-compose down
docker-compose up -d --build
