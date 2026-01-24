#!/bin/bash
cd /var/www/apps/new_start_up
git pull origin main
docker-compose down
docker-compose up -d --build
