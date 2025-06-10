from django.http import HttpResponse

# Create your views here.
def hello_view(request, name):
    return HttpResponse(f"<h1>Hello, {name}!</h1>")


def home_view(request):
    return HttpResponse("<h1>Добро пожаловать в мой Django-проект!</h1>")




