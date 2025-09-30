from task.models.base import BasicClass
from django.db import models

LANGUAGE_CHOICES = (
    ('english', "English"),
    ("russian", "Russian"),
    ("arabic", "Arabic"),
    ("turkish", "Turkish")

)


class Language(BasicClass):
    name = models.CharField(max_length=100, choices=LANGUAGE_CHOICES)

    def __str__(self):
        return self.name
