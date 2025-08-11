from django.db import models
from task.models import BasicClass
from django.core.validators import URLValidator, RegexValidator


class Vocab(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    word_1 = models.CharField(max_length=150)
    word_uz = models.CharField(max_length=150)
    text = models.TextField()

    def __str__(self):
        return f"{self.word_1} -- {self.word_uz}"


class Language(BasicClass):
    name = models.CharField(max_length=100)
    vocab = models.ForeignKey(Vocab, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Book(BasicClass):
    name = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(max_length=200, validators=[URLValidator(schemes='https')])

    def __str__(self):
        return self.name

