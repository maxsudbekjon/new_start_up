from typing import NamedTuple
from task.models.task import Task
from task.models.complete_task import CompleteTask
from task.utils import calculate_streak
class TaskLimitResult(NamedTuple):
    allowed: bool
    max_allowed: int | None
    message: str | None


def validate_task_count(*, user, program, count) -> TaskLimitResult:
    # 1. bitta programga bitta task
    if Task.objects.filter(program=program).exists():
        return TaskLimitResult(
            allowed=False,
            max_allowed=None,
            message="Bitta ilovaga 1 ta task"
        )

    age = user.age
    base_limits = {
        "child": 5,
        "teen": 10,
        "adult": 15,
    }

    completions = (
        CompleteTask.objects
        .filter(user=user)
        .order_by("completed_at")
        .values_list("completed_at", flat=True)
    )

    streak = calculate_streak(list(completions))
    bonus = 3 if streak >= 1 else 0

    if age <= 10:
        limit = base_limits["child"] + bonus
        label = "10 yoshdan kichiklar"
    elif age < 20:
        limit = base_limits["teen"] + bonus
        label = "10 va 19 yoshgacha"
    else:
        limit = base_limits["adult"] + bonus
        label = "20 yoshdan kattalar"

    if count > limit:
        return TaskLimitResult(
            allowed=False,
            max_allowed=limit,
            message=f"{label} uchun maksimal {limit}"
        )

    return TaskLimitResult(True, None, None)