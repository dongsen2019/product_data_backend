from django.shortcuts import render, HttpResponse, redirect
from login_app.models import *
from django.db.models import Q, F

# Create your views here.


def index(request):
    if request.method == "GET":

        response_home = redirect('product_display:index')

        user_session = request.session.get('user', None)

        if user_session is None:

            print(request.GET.get("account"))
            print(request.GET.get("pwd"))

            if request.GET.get("account") is None and request.GET.get("pwd") is None:
                return render(request, 'login_app/login/login.html')
            else:
                if User.objects.filter(Q(account=request.GET.get("account")) & Q(password=request.GET.get("pwd"))).exists():
                    request.session['user'] = {'account': request.GET.get("account"), 'pwd': request.GET.get("pwd"), }
                    return response_home
                else:
                    context = {
                        'pwd_error': '<span class="hint" style="display: block; color: red; margin-top: 23px">密码错误</span>'
                    }
                    return render(request, 'login_app/login/login.html', context=context)

        else:
            return response_home

    elif request.method == "POST":
        print(request.POST)
        return HttpResponse("POST Defined")



