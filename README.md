# Git va Docker buyruqlari
--------------------------

## 1. Git pull qilish

```bash
git pull origin main
```

## 2. env.exmple fayldan .env nusxa olish
```bash
cp env.example .env
```

## 3. .env faylni  to'ldirish
```bash
SECRET_KEY=
DEBUG=True

DB_TYPE=SQLITE
DB_NAME=neocontrol_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

```bash
SECRET_KEY berish kerak  
DB_TYPE=POSTGRES ga o\'zgartirish kerak 
```

## 4. Docker kontainerlarni ishga tushirish

```bash
docker-compose up --build
```

yoki

```bash
docker compose up --build
```
