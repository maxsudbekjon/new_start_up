from task.models.base import BasicClass
from django.db import models
from .vocab import Vocab

class Language(BasicClass):
    name = models.CharField(max_length=100)
    vocab = models.ForeignKey(Vocab, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
