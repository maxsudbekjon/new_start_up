from django.contrib import admin
from .models import Do, Program, Task, CompleteTask

@admin.register(CompleteTask)
class CompleteTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "task", "completed_at", "spent_time")
    list_filter = ("completed_at", "user")
    search_fields = ("task__title", "user__username")
    ordering = ("-completed_at",)
    fields = ("user", "task", "completed_at", "spent_time")


admin.site.register([Do, Program, Task])
