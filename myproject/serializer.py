from rest_framework import serializers
from .models import Task, SubTask, Category
from django.utils import timezone


class TaskCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True)

    class Meta:
        model = Task
        fields = ['title',
            'description',
            'status',
            'deadline',
            'publish_date',
            'categories',
                  ]

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Дата дедлайна не может быть в прошлом.")
        return value


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'created_at', 'task', 'deadline']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        """Проверка уникальности названия при создании или обновлении"""
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Категория с таким названием уже существует.")
        return value

    def create(self, validated_data):
        """Вызывается при POST-запросе"""
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        """Проверяем уникальность названия"""
        if Category.objects.exclude(pk=instance.pk).filter(name=name).exists():
            raise serializers.ValidationError({"name": "Категория с таким названием уже существует."})
        setattr(instance, 'name', name)
        instance.save()
        return instance

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskCreateSerializer(read_only=True, many=True)
    categories = CategoryCreateSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'subtasks', 'status', 'deadline', 'publish_date', 'categories']