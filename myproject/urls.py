from django.urls import path
from myproject.views import home_view, hello_view

urlpatterns = [
    path('', home_view, name='home'),  # Главная страница
    path('hello/<str:name>/', hello_view, name='hello'),
]

