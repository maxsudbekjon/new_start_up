from task.models.base import BasicClass
from django.db import models
from django.conf import settings


class Book(BasicClass):
    name = models.CharField(max_length=100)
    description = models.TextField()
    book = models.FileField(upload_to='book/')

    def __str__(self):
        return self.name


class BookProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    last_page = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user} - {self.book} >>> last_page: ({self.last_page})"
