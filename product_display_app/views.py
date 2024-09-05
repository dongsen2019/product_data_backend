from django.shortcuts import render, HttpResponse
from product_display_app.models import *
from django.db.models import Q
import os
from product_data_backend import settings


def func_display(request):
    return render(request, "product_display_app/function_display/function_display.html")


# Create your views here.
def index(request):
    if request.method == "GET":
        print(request.GET.dict())
        para_dict = request.GET.dict()
        gjm = para_dict.get("gjm")
        sptm = para_dict.get("sptm")
        ftm = para_dict.get("ftm")

        info_empty = {"name": ("", ""), "group_sn": ("国际码: ", ""), "brand_alias": ("品牌别名: ", ""),
                      "dept_name": ("大类: ", ""), "big_category_name": ("中类: ", ""),
                      "small_category_name": ("小类: ", ""), "col": ("颜色:", ""), "season": ("季节", ""),
                      "gender": ("性别: ", ""), "market_price": ("市场价: ", "")}

        # 当 GET 参数为空 或者 无GET参数(字典为空时)
        if request.GET.dict() == {} or (gjm == "" and sptm == "" and ftm == ""):
            context = {
                "get_para": 0,
                "images_path": ["/static/assets/src-images/blank.jpg" for i in range(9)],
                "info": info_empty,
                # "map": {"name": "", "barcode": "商品条码", "group_sn": "国际码", "brand_alias": "品牌别名", "dept_name": "大类",
                #         "big_category": "中类", "small_category": "小类", "col": "颜色", "size": "尺寸", "season": "季节",
                #         "gender": "性别", "market_price": "市场价"},
                "numbers_image": range(9),
                "numbers_info": range(12),
            }

            return render(request, "product_display_app/product_display/product_display_new.html", context=context)

        else:

            # 原生sql语句查询
            g_sn = gjm
            result = PDC.objects.raw("SELECT * FROM (SELECT * FROM product_display_app_pdc t1 where group_sn = %s limit 1) t1 left join product_display_app_samestyle_detail t2 on t1.group_sn = t2.group_sn", [g_sn])
            print(len(result))
            for i in result:
                print(i.same_style)

            """
            # 使用django的queryset查询
            
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
            """

            # print(result)

            # 如果数据库查询的返回结果是0条数据,就返回空字符集字典, 国际码设置为空
            if len(result) == 0:
                product_info = {"group_sn": ""}

                info_dict = info_empty
            else:
                """
                # 使用 django 的 queryset 查询
                
                product_info = result[0]

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
                """
                info_dict = {
                    "name": ("", result[0].name),
                    "group_sn": ("国际码: ", result[0].group_sn),
                    "brand_alias": ("品牌别名: ", result[0].brand_alias),
                    "dept_name": ("大类: ", result[0].dept_name),
                    # "big_category_name": ("中类: ", result[0].big_category_name),
                    "small_category_name": ("小类: ", result[0].small_category_name),
                    "size": ("尺寸: ", result[0].size),
                    "same_style": ("同款: ", result[0].same_style),
                    "mark": ("标识: ", result[0].mark),
                    "is_double": ("双面: ", result[0].is_double),
                    "disassembly": ("扣头是否拆卸: ", result[0].disassembly),
                    "length": ("长短: ", result[0].length),
                    "col": ("颜色:", result[0].col),
                    "season": ("季节: ", result[0].season),
                    "gender": ("性别: ", result[0].gender),
                    "market_price": ("市场价: ", result[0].market_price),
                }

            # print(info_dict)

            # 取商品图片

            # 绝对路径
            # print(os.path.join(settings.STATICFILES_DIRS[0], "assets", "product_images", product_info.get("group_sn")))

            # 相对路径
            # 静态static路径千万记得要 /static 别忘了加前面的斜杠
            print(os.path.isdir(os.path.join(settings.STATIC_URL, "assets", "product_images", result[0].group_sn)))
            images_path = os.path.join(settings.STATIC_URL, "assets", "product_images", result[0].group_sn, "750")
            static_images_path = os.path.join("assets", "product_images", result[0].group_sn, "750")
            is_exists = os.path.isdir(images_path)

            # 如果路径的存在,获取路径下的所有文件
            images_path_list = []
            if is_exists is True:
                images_list = os.listdir(images_path)
                print(images_list)

                del_ele = []
                # 去除缓存文件
                for file in images_list:
                    if not ((file.endswith(".jpg")) or (file.endswith(".png"))):
                        del_ele.append(file)

                print(del_ele)
                for ele in del_ele:
                    images_list.remove(ele)

                print(images_list)

                images_count = len(images_list)

                # print(images_count) 如果 images_count 大于 9, 则设置数量为 9

                if images_count > 9:
                    images_count = 9

                # print(images_count)

                for image_i in range(images_count):
                    # images_path_list.append(os.path.join("/", images_path, images_list[image_i]))
                    images_path_list.append([result[0].group_sn, images_list[image_i], os.path.join(static_images_path, images_list[image_i])])  # 使用静态链接的方法
            else:
                for i in range(9):
                    images_path_list.append(["empty", "blank.jpg", "/assets/src-images/blank.jpg"])

            # print(len(images_path_list))

            # 如果图片数量小于9, 则计算剩余的空白图片数量
            surplus = 9 - len(images_path_list)

            # 如果剩余数不为0,则追加空白图片链接地址
            if surplus != 0:
                for i in range(surplus):
                    images_path_list.append(["empty", "blank.jpg", "/assets/src-images/blank.jpg"])

            context = {
                "get_para": 1,
                "images_path": images_path_list,
                "info": info_dict,
                "numbers_image": range(9),
                "surplus_image": surplus,
                "numbers_info": range(12),
                "list_address": request.scheme + "://" + request.get_host() + "/product_display/tmzs/list/" + info_dict["same_style"][1],
            }

            print(context["images_path"])

            return render(request, "product_display_app/product_display/product_display_new.html", context=context)

    elif request.method == "POST":
        return HttpResponse("POST Defined")


def image_display(request, group_sn, path_image):
    print(group_sn, path_image)
    if group_sn != "empty":
        image_link = os.path.join("assets", "product_images", group_sn, "750", path_image)
        context = {
            "image_link": image_link
        }
        return render(request, 'product_display_app/image_display/image_display.html', context=context)
    else:
        image_link = os.path.join("assets", "src-images", "blank.jpg")
        context = {
            "image_link": image_link
        }
        return render(request, 'product_display_app/image_display/image_display.html', context=context)


def list_display(request, group_sn):
    # print(request.scheme)
    # print(request.get_host())
    # print(group_sn)

    result = SameStyle_Detail.objects.filter(same_style=group_sn).values()

    for i in result:
        g_sn = i["group_sn"]
        i["link"] = request.scheme + "://" + request.get_host() + "/product_display/tmzs?gjm=" + g_sn + "&sptm=&ftm="

    content = {
        "item_list": result
    }

    # print(result)

    return render(request, 'product_display_app/list_display/list_display.html', context=content)

