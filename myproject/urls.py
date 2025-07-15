from django.urls import path
from myproject.views import home_view, hello_view, task_create, task_list, task_detail, task_count, task_stats

urlpatterns = [
    # path('', home_view, name='home'),  # Главная страница
    path('hello/<str:name>/', hello_view, name='hello'),
    path('create/', task_create),
       # Маршрут для создания нового задания
    path('', task_list, name='task_list'),
    # Маршрут для получения всех заданий
    path('<int:pk>/',task_detail, name='task_detail'),
    # Маршрут для получения одного задания
    path('count/', task_count, name='task_count'),
    path('stats/', task_stats, name='task_stats'),
]

