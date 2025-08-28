from django.contrib import admin
from .models import  Task, CompleteTask, Do, Program

admin.site.register([ Task, CompleteTask,Do, Program])
