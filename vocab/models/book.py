from task.models.base import BasicClass
from django.db import models
from django.core.validators import URLValidator

class Book(BasicClass):
    name = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(max_length=200, validators=[URLValidator(schemes='https')])

    def __str__(self):
        return self.name