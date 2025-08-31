from task.models.base import BasicClass
from django.db import models

class Language(BasicClass):
    name = models.CharField(max_length=100)
    vocab = models.ForeignKey('vocab.Vocab', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
