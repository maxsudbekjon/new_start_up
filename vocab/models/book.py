from task.models.base import BasicClass
from django.db import models


class Book(BasicClass):
    name = models.CharField(max_length=100)
    description = models.TextField()
    book = models.FileField(upload_to='book/')

    def __str__(self):
        return self.name


class BookProgress(BasicClass):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="book_progress")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="progress")
    last_page = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "book")

    def __str__(self):
        return f"{self.user_id}:{self.book_id}"
