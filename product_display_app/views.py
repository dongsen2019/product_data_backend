from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    return render(request, "product_display_app/product_display/product_display.html")