from django.contrib import admin
from .models import Task, SubTask, Category

# Register your models here.


# admin.site.register(SubTask)
# admin.site.register(Category)
# admin.site.register(Task)
class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title',  'status', 'deadline', 'created_at')
    # Задание полей, по которым будет производиться поиск
    list_filter = ('status', 'deadline', 'categories')
    # позволяет фильтровать по статусу, категориям и задачам
    search_fields = ('title', 'description')
    # упрощает поиск по названию и описанию
    ordering = ('-created_at',)
    # задает порядок сортировки записей
    filter_horizontal = ('categories',)
#     улучшает выбор ManyToMany-связей
    inlines = [SubTaskInline]

    def short_title(self, obj):
        return (obj.title[:10] + '...') if len(obj.title) > 10 else obj.title
    short_title.short_description = 'Задача'

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'task')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    actions = ['mark_done']

    @admin.action(description='Пометить как выполненные (Done)')
    def mark_done(self, request, queryset):
        updated = queryset.update(status='Done')
        self.message_user(request, f'✅ Обновлено задач: {updated}')



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)



