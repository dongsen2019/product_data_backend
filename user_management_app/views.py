from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    return render(request, "user_management_app/user_management/user_management.html")
