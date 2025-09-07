from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CompleteTask, Task
from django.utils.timezone import now


@receiver(post_save, sender=Task)
def create_complete_task_and_check_streak(sender, instance, created, **kwargs):
    task = instance

    if task.is_complete:
        CompleteTask.objects.get_or_create(
            task=task,
            user=task.user,
            defaults={"completed_at": now()}
        )
