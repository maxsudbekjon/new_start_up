from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqami +998 bilan boshlanib, jami 13 ta raqamdan iborat bo‘lishi kerak (masalan: +998901254456)"
)

phone_pattern = r'^\+?\d{9,15}$'