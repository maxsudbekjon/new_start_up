
from .program import *

class Task(BasicClass):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    duration = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title