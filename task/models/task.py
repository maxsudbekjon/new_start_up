from .base import *

class Task(BasicClass):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    duration = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Program(BasicClass):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Do(BasicClass):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title