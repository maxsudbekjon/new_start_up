
from .base import *

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
class Task(BasicClass):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,verbose_name='user',related_name='tasks')
    title = models.ForeignKey('task.Do',on_delete=models.CASCADE,verbose_name='do',related_name='tasks')
    program = models.ForeignKey('task.Program', on_delete=models.CASCADE,verbose_name='program',related_name='tasks')
    count = models.IntegerField(default=0)
    duration = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title