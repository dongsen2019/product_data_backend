from django.shortcuts import redirect, HttpResponse
from django.conf import settings
# 在你的应用程序目录下创建 middleware.py 文件
# myapp/middleware.py


class SessionValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 获取当前请求路径
        current_path = request.path_info
        # print(current_path)
        # print(request.session.get('user'))

        # 如果用户未登录且当前路径不是登录页面，重定向到登录页面  not True = False \ None 不要混淆 not 和 取非 !
        if not request.session.get('user', None) and current_path != settings.LOGIN_URL:  # 少了右边的条件就会进入无限重定向循环
            return redirect(settings.LOGIN_URL)

        # 继续处理请求
        response = self.get_response(request)
        return response
