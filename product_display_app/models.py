from django.db import models

# Create your models here.


class PDC(models.Model):
    barcode = models.CharField("商品条码", max_length=100)
    parent_barcode = models.CharField("父条码", max_length=100)
    group_sn = models.CharField("国际码", max_length=100)
    name = models.CharField("商品名称", max_length=100)
    col = models.CharField("颜色", max_length=50)
    size = models.CharField("尺寸", max_length=50)
    dept_name = models.CharField("大类", max_length=50)
    big_category_name = models.CharField("中类", max_length=50)
    small_category_name = models.CharField("小类", max_length=50)
    season = models.CharField("季节", max_length=50)
    gender = models.CharField("性别", max_length=50)
    market_price = models.FloatField(verbose_name="市场价")
    brand_alias = models.CharField("品牌别名", max_length=50)


class SameStyle_Detail(models.Model):
    group_sn = models.CharField("国际码", max_length=100)
    same_style = models.CharField("同款名称", max_length=50)
    size = models.CharField("尺寸", max_length=50)
    is_double = models.CharField("双面", max_length=50)
    disassembly = models.CharField("扣头拆卸", max_length=50)
    mark = models.CharField("标识", max_length=50)
    length = models.CharField("长短", max_length=50)
