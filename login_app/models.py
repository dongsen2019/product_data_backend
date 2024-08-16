from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator


# Create your models here.
class User(models.Model):
    full_name = models.CharField("姓名", max_length=20)
    department = models.CharField("部门", max_length=20)
    account = models.CharField("账号", max_length=20)
    password = models.CharField("密码", max_length=20)

