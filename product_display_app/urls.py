from django.urls import path
from product_display_app.views import *

app_name = "product_display"

# 子路由去掉总路由的前缀路径
urlpatterns = [
    # 固定路径路由, 不带动态参数设计方案
    path('', func_display, name='func_display'),
    path('tmzs', index, name='index'),
    path('tmzs/<str:group_sn>/<str:path_image>', image_display, name='image_display')
]
