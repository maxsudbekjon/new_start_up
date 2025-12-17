##############################
# 1-STAGE: BUILDER
##############################
FROM python:3.12-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


##############################
# 2-STAGE: RUNTIME
##############################
FROM python:3.12-slim
WORKDIR /app

RUN useradd -m django

COPY --from=builder /usr/local /usr/local
COPY . .
RUN chown -R django:django /app

USER django

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

