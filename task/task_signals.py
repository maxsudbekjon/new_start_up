from django.db.models.signals import post_save
from django.dispatch import receiver
from task.models.task import Task
from task.models.complete_task import CompleteTask


@receiver(post_save, sender=Task)
def create_complete_task(sender, instance, created, **kwargs):
    if instance.is_complete:
        CompleteTask.objects.get_or_create(task=instance)
