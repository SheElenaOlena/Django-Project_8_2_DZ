from django.urls import path, include
from myproject.views import (FilteredSubTaskListApiView,SubTaskListApiView,
                             TaskView, home_view, hello_view, task_create,
                             task_list, task_detail, task_count, task_stats)

urlpatterns = [
    # path('', home_view, name='home'),  # Главная страница
    path('hello/<str:name>/', hello_view, name='hello'),
    path('create/', task_create),
       # Маршрут для создания нового задания
    path('', TaskView.as_view(), name='task-list'),
    path('all/', task_list, name='task_list'),
    # Маршрут для получения всех заданий
    path('<int:pk>/',task_detail, name='task_detail'),
    # Маршрут для получения одного задания
    path('count/', task_count, name='task_count'),
    path('stats/', task_stats, name='task_stats'),
    path('subtasks/', SubTaskListApiView.as_view(), name='subtasks-list'),  # /api/v1/tasks/subtasks/
    path('subtasks/filtered/', FilteredSubTaskListApiView.as_view(), name='subtask-filtered'),

]


