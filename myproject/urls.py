from django.urls import path, include
from myproject.views import (CategoryRetrieveUpdateDestroyAPIView, CategoryListCreateAPIView,
                             SubTaskDetailUpdateDeleteView,SubTaskListCreateAPIView,
                             TaskRetrieveUpdateDestroyAPIView, TaskListCreateAPIView,
                             FilteredSubTaskListApiView,SubTaskListApiView,
                             TaskView, home_view, hello_view, task_create,
                             task_list, task_detail, task_count, task_stats)

# urlpatterns = [
#     # path('', home_view, name='home'),  # Главная страница
#     path('hello/<str:name>/', hello_view, name='hello'),
#     # path('create/', task_create),
#        # Маршрут для создания нового задания
#     path('analytics/', TaskView.as_view(), name='task-list'),
#     # path('all/', task_list, name='task_list'),
#     # Маршрут для получения всех заданий
#     # path('<int:pk>/',task_detail, name='task_detail'),
#     # Маршрут для получения одного задания
#     path('count/', task_count, name='task_count'),
#     path('stats/', task_stats, name='task_stats'),
#     # path('subtasks/', SubTaskListApiView.as_view(), name='subtasks-list'),  # /api/v1/tasks/subtasks/
#     # path('subtasks/filtered/', FilteredSubTaskListApiView.as_view(), name='subtask-filtered'),
#     # path('', TaskListCreateAPIView.as_view(), name='task-list-create'),
#     path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
#     path('subtasks/', SubTaskListCreateAPIView.as_view(), name='subtask-list-create')
#
#
#
# ]
urlpatterns = [
    # Список задач и создание
    path('', TaskListCreateAPIView.as_view(), name='task-list-create'),

    # Детальный просмотр, обновление, удаление задачи
    path('<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),

    # Статистика и аналитика
    path('count/', task_count, name='task-count'),
    path('stats/', task_stats, name='task-stats'),

    # Список подзадач + создание
    path('subtasks/', SubTaskListCreateAPIView.as_view(), name='subtask-list-create'),

    # Фильтр подзадач
    path('subtasks/filtered/', FilteredSubTaskListApiView.as_view(), name='subtask-filtered'),

    # Обновление и удаление конкретной подзадачи
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
 # Список категорий и создание новой
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),

    # Получение, обновление и удаление конкретной категории
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
]


