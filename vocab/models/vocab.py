
from django.db import models

class Vocab(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    word_1 = models.CharField(max_length=150)
    word_uz = models.CharField(max_length=150)
    text = models.TextField()

    def __str__(self):
        return f"{self.word_1} -- {self.word_uz}"