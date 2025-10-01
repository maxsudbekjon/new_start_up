from .task import *


class CompleteTask(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    spent_time = models.IntegerField(default=0)  

    def __str__(self):
        return str(self.task.title)

