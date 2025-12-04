from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from task.models import BasicClass
from helpers.validators import phone_pattern, phone_validator
from django.core.exceptions import ValidationError
import re


class CustomUserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValidationError('Phone is required')

        # phone validator
        if not re.match(phone_pattern, phone):
            raise ValidationError({"phone": "Telefon raqami noto‘g‘ri formatda!"})

        extra_fields['phone'] = phone

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)



class User(AbstractUser, BasicClass):
    LEVEL_CHOICES = (
        ('initial', "Boshlang'ich"),
        ('medium', "O'rta"),
        ('high', 'Yuqori')
    )

    username = models.CharField(max_length=255, unique=True,null=True,blank=True)
    phone = models.CharField(
        max_length=255,
        validators=[phone_validator],
        unique=True
    )
    age = models.IntegerField(default=0)
    level = models.CharField(max_length=255, choices=LEVEL_CHOICES, null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.phone}"


