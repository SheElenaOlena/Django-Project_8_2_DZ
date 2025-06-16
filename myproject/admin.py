from django.contrib import admin
from .models import Task, SubTask, Category

# Register your models here.


# admin.site.register(SubTask)
# admin.site.register(Category)
# admin.site.register(Task)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    # Задание полей, по которым будет производиться поиск
    list_filter = ('status', 'deadline', 'categories')
    # позволяет фильтровать по статусу, категориям и задачам
    search_fields = ('title', 'description')
    # упрощает поиск по названию и описанию
    ordering = ('-created_at',)
    # задает порядок сортировки записей
    filter_horizontal = ('categories',)
#     улучшает выбор ManyToMany-связей

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'task')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)