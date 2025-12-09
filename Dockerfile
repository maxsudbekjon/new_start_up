##############################
# 1-STAGE: BUILDER (og‘ir qism)
##############################
FROM python:3.12-slim AS builder

# 1) Ishchi katalog
WORKDIR /app

# 2) Build uchun zarur system deps
# Bu bosqichda kompilyatsiya bo‘lishi mumkin bo‘lgan kutubxonalar uchun
# gcc, build-essential, libpq-dev o‘rnatiladi.
# Ammo ular faqat BUILD paytida kerak, RUN paytida aslo kerak emas.
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 3) Requirements'larni o‘rnatamiz, faqat builder bosqichida
# --user: kutubxonalarni /root/.local joyiga o‘rnatadi
# Bu keyin runtime image’ga bitta COPY bilan ko‘chirishni osonlashtiradi.
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt



##############################
# 2-STAGE: RUNTIME (yengil qism)
##############################
FROM python:3.12-slim

# 4) Ishchi katalog
WORKDIR /app

# 5) Linux user yaratamiz (optional, security uchun)
# Root bo‘lmagan user bilan appni ishga tushirish xavfsizroq.
RUN useradd -m django

# 6) Builder stage'dan FAQAT kerakli Python kutubxonalarini ko‘chiramiz
# Mana shu qator multi-stage buildning eng muhim joyi
# build-essential, libpq-dev, gcc... Hech biri final imagega o'tmaydi!
COPY --from=builder /root/.local /root/.local

# 7) PATH'ni yangilash — pip user install qilgan joyni ko‘rsatamiz
ENV PATH=/root/.local/bin:$PATH

# 8) Loyihadagi source code'ni ko‘chiramiz
COPY . .

# 9) Root bo‘lmagan userga o‘tkazamiz
USER django

# 10) Gunicorn orqali ishga tushirish
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
