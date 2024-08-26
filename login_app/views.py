import datetime
from django.shortcuts import render, HttpResponse, redirect
from login_app.models import *
from django.db.models import Q, F
from django.contrib.sessions.models import Session

# Create your views here.


def index(request):
    if request.method == "GET":
        response_home = redirect('product_display:func_display')

        user_session = request.session.session_key
        # print(f"user_session是否为空:{user_session}")
        # print(request.session.values())

        # 如果 user_session
        if user_session is not None:
            for s in Session.objects.values():
                # print(f"1:{s["session_key"] == user_session}")
                # print(f"2:{s["expire_date"] > datetime.datetime.now()}")
                if s["session_key"] == user_session:
                    if s["expire_date"] > datetime.datetime.now():
                        return response_home
                    else:
                        # request.session.delete() # 过期的session,django在重定向后自动清理
                        return render(request, 'login_app/login/login.html')

        # user_session = request.session.get('user', None) # 从session中获取曾今设置过的用户信息user

        # print(request.session.values())
        # print(request.session.session_key)

        # print(Session.objects.values())

        elif user_session is None:
            # print(request.GET.get("account"))  账号
            # print(request.GET.get("pwd"))  密码

            if user_session is None:
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
                return HttpResponse("session表中, 无此session_key")

    elif request.method == "POST":
        print(request.POST)
        return HttpResponse("POST Defined")



