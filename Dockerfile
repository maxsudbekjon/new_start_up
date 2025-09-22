FROM python:3.12-slim

# Ishchi katalog
WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

# Source code
COPY . .

# Gunicorn orqali ishga tushirish
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
