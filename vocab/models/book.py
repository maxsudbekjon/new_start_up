from task.models.base import BasicClass
from django.db import models


class Book(BasicClass):
    name = models.CharField(max_length=100)
    description = models.TextField()
    book=models.FileField(upload_to='book')

    def __str__(self):
        return self.name