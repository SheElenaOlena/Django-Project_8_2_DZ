from django.db.models.aggregates import Count
from django.http import HttpResponse
from rest_framework.generics import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task, SubTask
from .serializer import TaskCreateSerializer, TaskDetailSerializer, SubTaskCreateSerializer
from django.utils import timezone


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


class SubTaskListCreateView(APIView):
    """Представление для списка и создания подзадач"""
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




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
