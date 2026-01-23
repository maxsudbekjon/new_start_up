from celery import shared_task
from task.models.task import Task


@shared_task
def reset_active_tasks_daily():
    # Reset completion status for all active tasks
    Task.objects.filter(is_active=True).update(is_complete=False)
