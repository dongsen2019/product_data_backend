from django.urls import path
from login_app.views import *

app_name = "login"

# 子路由去掉总路由的前缀路径
urlpatterns = [
    # 固定路径路由, 不带动态参数设计方案
    path('', index, name='index'),
]