from django.shortcuts import render, HttpResponse
from product_display_app.models import *
from django.db.models import Q
import os
from product_data_backend import settings


# Create your views here.
def index(request):
    if request.method == "GET":
        print(request.GET.dict())
        para_dict = request.GET.dict()
        gjm = para_dict.get("gjm")
        sptm = para_dict.get("sptm")
        ftm = para_dict.get("ftm")

        # 当 GET 参数为空 或者 无GET参数(字典为空时)
        if request.GET.dict() == {} or (gjm == "" and sptm == "" and ftm == ""):
            context = {
                "get_para": 0,
                "images_path": ["/static/assets/src-images/blank.jpg" for i in range(9)],
                "info": {"name": ("", ""), "group_sn": ("国际码: ", ""),
                         "brand_alias": ("品牌别名: ", ""), "dept_name": ("大类: ", ""), "big_category_name": ("中类: ", ""),
                         "small_category_name": ("小类: ", ""), "col": ("颜色:", ""), "season": ("季节", ""),
                         "gender": ("性别: ", ""), "market_price": ("市场价: ", "")},
                # "map": {"name": "", "barcode": "商品条码", "group_sn": "国际码", "brand_alias": "品牌别名", "dept_name": "大类",
                #         "big_category": "中类", "small_category": "小类", "col": "颜色", "size": "尺寸", "season": "季节",
                #         "gender": "性别", "market_price": "市场价"},
                "numbers_image": range(9),
                "numbers_info": range(12),
            }

            return render(request, "product_display_app/product_display/product_display.html", context=context)

        else:
            # 当GET参数不为空时, 取商品PDC信息
            Q_gjm = Q()
            Q_sptm = Q()
            Q_ftm = Q()

            # 不为空的参数构建Q表达式
            print(gjm, sptm, ftm)
            if gjm != "":
                Q_gjm = Q(group_sn=gjm)
                print(Q_gjm)

            if sptm != "":
                Q_ftm = Q(barcode=sptm)
                print(Q_ftm)

            if ftm != "":
                Q_sptm = Q(parent_barcode=ftm)
                print(Q_ftm)

            Q_filter = Q_gjm & Q_sptm & Q_ftm

            print(Q_filter)

            result = PDC.objects.filter(Q_filter).values()

            product_info = result[1]

            info_dict = {
                "name": ("", product_info.get("name")),
                "group_sn": ("国际码: ", product_info.get("group_sn")),
                "brand_alias": ("品牌别名: ", product_info.get("brand_alias")),
                "dept_name": ("大类: ", product_info.get("dept_name")),
                "big_category_name": ("中类: ", product_info.get("big_category_name")),
                "small_category_name": ("小类: ", product_info.get("small_category_name")),
                "col": ("颜色:", product_info.get("col")),
                "season": ("季节", product_info.get("season")),
                "gender": ("性别: ", product_info.get("gender")),
                "market_price": ("市场价: ", product_info.get("market_price")),
            }

            # print(info_dict)

            # 取商品图片

            # 绝对路径
            # print(os.path.join(settings.STATICFILES_DIRS[0], "assets", "product_images", product_info.get("group_sn")))

            # 相对路径
            # 静态static路径千万记得要 /static 别忘了加前面的斜杠
            print(os.path.isdir(os.path.join(settings.STATIC_URL, "assets", "product_images", product_info.get("group_sn"))))
            images_path = os.path.join(settings.STATIC_URL, "assets", "product_images", product_info.get("group_sn"), "750")
            is_exists = os.path.isdir(images_path)

            images_path_list = []
            if is_exists is True:
                print(os.listdir(images_path))
                images_list = os.listdir(images_path)
                print(images_list)

                if 'Thumbs.db' in images_list:
                    images_list.remove('Thumbs.db')

                images_count = len(images_list)

                # print(images_count)

                if images_count > 9:
                    images_count = 9

                # print(images_count)

                for image_i in range(images_count):
                    images_path_list.append(os.path.join("/", images_path, images_list[image_i]))
            else:
                for i in range(9):
                    images_path_list.append("/static/assets/src-images/blank.jpg")

            print(len(images_path_list))

            surplus = 9 - len(images_path_list)

            if surplus != 0:
                for i in range(surplus):
                    images_path_list.append("/static/assets/src-images/blank.jpg")

            context = {
                "get_para": 1,
                "images_path": images_path_list,
                "info": info_dict,
                "numbers_image": range(9),
                "surplus_image": surplus,
                "numbers_info": range(12),
            }

            return render(request, "product_display_app/product_display/product_display.html", context=context)

    elif request.method == "POST":
        return HttpResponse("POST Defined")

