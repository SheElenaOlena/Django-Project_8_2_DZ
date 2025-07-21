from django.core.serializers import serialize
from django.db.models.aggregates import Count
from django.db.models.expressions import result
from django.http import HttpResponse
from rest_framework.generics import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task, SubTask, Category
from .serializer import (CategorySerializer, SubTaskDetailSerializer, TaskSerializer,
                         TaskCreateSerializer, TaskDetailSerializer,
                         SubTaskCreateSerializer, CategoryCreateSerializer)
from django.utils import timezone
from django.db.models.functions import ExtractWeekDay
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend




# Create your views here.
def hello_view(request, name):
    return HttpResponse(f"<h1>Hello, {name}!</h1>")


def home_view(request):
    return HttpResponse("<h1>Добро пожаловать в мой Django-проект!</h1>")


@api_view(['POST'])
def task_create(request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskCreateSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TaskDetailSerializer(task)
    return Response(serializer.data)


@api_view(['GET'])
def task_count(request):
    count = Task.objects.count()
    return Response({'total_tasks': count})


@api_view(['GET'])
def task_stats(request):
    now = timezone.now()
    stats = {
        "new": Task.objects.filter(status="New").count(),
        "in_progress": Task.objects.filter(status="In progress").count(),
        "done": Task.objects.filter(status="Done").count(),
        "pending": Task.objects.filter(status="Pending").count(),
        "blocked": Task.objects.filter(status="Blocked").count(),
        "overdue": Task.objects.filter(deadline__lt=now).count(),
    }
    return Response(stats)

class TaskDetailAPIView(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer



class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer



# class SubTaskListCreateView(APIView):
#     """Представление для списка и создания подзадач"""
#     def get(self, request):
#         subtasks = SubTask.objects.all()
#         serializer = SubTaskCreateSerializer(subtasks, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
class SubTaskListCreateAPIView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


class SubTaskDetailUpdateDeleteView(APIView):
    """Представление для деталей, обновления и удаления"""
    def get(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class TaskView(APIView):
    def get(self, request):
        day_param = request.query_params.get('day', None)

        # Словарь: день недели → номер для ExtractWeekDay
        day_map = {
            'понедельник': 2,
            'вторник': 3,
            'среда': 4,
            'четверг': 5,
            'пятница': 6,
            'суббота': 7,
            'воскресенье': 1
        }

        tasks = Task.objects.all().annotate(
            week_day=ExtractWeekDay('created_at')  # или 'publish_date'
        )

        if day_param:
            day_param_lower = day_param.lower()
            day_number = day_map.get(day_param_lower)
            if day_number:
                tasks = tasks.filter(week_day=day_number)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class SubTaskPagination(PageNumberPagination):
    """Пагинация данных """
    page_size = 5
    page_size_query_param = 'page_size'  # Позволяет задавать page_size через URL

class SubTaskListApiView(ListAPIView):
    """Пагинация подзадач с сортировкой по убыванию даты"""
    serializer_class = SubTaskDetailSerializer
    pagination_class = SubTaskPagination

    def get_queryset(self):
        parent_id = self.request.query_params.get('parent_task_id')
        queryset = SubTask.objects.all().order_by('-deadline')
        if parent_id:
            queryset = queryset.filter(parent_task_id=parent_id)
        return queryset

    """Получение списка всех подзадач по названию главной задачи
       и статусу подзадач с использованием фильтров"""
class FilteredSubTaskListApiView(ListAPIView):
    serializer_class = SubTaskDetailSerializer
    pagination_class = SubTaskPagination

    def get_queryset(self):
        """query-параметры запроса.
        Если они передаются — фильтрация применяется.
        Если не передаются — выводятся все записи."""

        main_task_title = self.request.query_params.get('main_task_title')
        status_param = self.request.query_params.get('status')

        queryset = SubTask.objects.all().order_by('-created_at')

        if main_task_title:
            queryset = queryset.filter(task__title__iexact=main_task_title)

        if status_param:
            queryset = queryset.filter(status__iexact=status_param)

        return queryset


class TaskListCreateAPIView(ListCreateAPIView):
    serializer_class = TaskCreateSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = Task.objects.all()

        # Фильтрация по статусу
        status_param = self.request.query_params.get('status')
        if status_param:
            status_cleaned = status_param.strip().lower()
            queryset = queryset.filter(status__iexact=status_cleaned)

        # Фильтрация по дедлайну
        deadline_param = self.request.query_params.get('deadline')
        if deadline_param:
            queryset = queryset.filter(deadline=deadline_param)

        return queryset



class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer