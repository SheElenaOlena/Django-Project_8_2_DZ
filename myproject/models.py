from django.utils import timezone

from .managers import SoftDeleteManager
from django.db import models

# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Done', 'Done'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
    ]
    title = models.CharField(max_length=100, verbose_name='Название задачи', unique=True,
                             unique_for_date='publish_date', null=False, blank=False)
    description = models.TextField(verbose_name='Описание задачи', null=False, blank=False)
    categories = models.ManyToManyField('Category', verbose_name='Категории', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    deadline = models.DateTimeField(verbose_name='Дедлайн', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    publish_date = models.DateField(verbose_name='Дата публикации')

    def __str__(self):
        return f"{self.title} ({self.publish_date})"

    class Meta:
        db_table = 'task_manager_task'  # Задаем имя таблицы в базе данных
        ordering = ['-created_at']  # Сортировка по убыванию даты создания
        verbose_name = 'Task'  # Человекочитаемое имя модели




class SubTask(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Done', 'Done'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
    ]
    title = models.CharField(max_length=100, verbose_name='Название подзадачи',
                              null=False, unique=True, blank=False)
    description = models.TextField(verbose_name='Описание подзадачи', null=False, blank=False)
    task =  models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks',
                                    verbose_name='Основная задача')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    deadline = models.DateTimeField(verbose_name='Дедлайн', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


    def __str__(self):
        return f"({self.title})"

    class Meta:
        db_table = 'task_manager_subtask'  # Задаем имя таблицы в базе данных
        ordering = ['-created_at']  # Сортировка по убыванию даты создания
        verbose_name = 'SubTask'  # Человекочитаемое имя модели



class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название категории')
    is_deleted = models.BooleanField(default=False)    # Поле для мягкого удаления
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')

    objects = SoftDeleteManager()   # Менеджер для исключения удаленных записей

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'  # Задаем имя таблицы в базе данных
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


