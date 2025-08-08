from django.contrib import admin
from .models import Do, Program, Task, CompleteTask

admin.site.register([Do, Program, Task, CompleteTask])
