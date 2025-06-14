from django.contrib import admin
from .models import Task, SubTask, Category

# Register your models here.


admin.site.register(SubTask)
admin.site.register(Category)
admin.site.register(Task)
