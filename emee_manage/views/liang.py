
from gettext import install
from dataclasses import fields
from django.shortcuts import render, HttpResponse, redirect
from emee_manage import models
from emee_manage.utils.pagination import Pagination
from emee_manage.utils.form import liangModelForm

# 靓号列表


def liang_list(req):
    search_value = req.GET.get("q", "")
    data_dict = {}
    if search_value:
        data_dict["mobile__contains"] = search_value

    liang = models.Liang.objects.filter(**data_dict).order_by("level")

    page_manage = Pagination(req, liang, "page")
    page_queryset = page_manage.page_queryset
    page_str = page_manage.html()

    return render(
        req,
        "liang_list.html",
        {
            "page_queryset": page_queryset,
            "search_value": search_value,
            "page_str": page_str,
            "req": req,
        }
    )

# 新建靓号


def liang_add(req):
    if req.method == "GET":
        form = liangModelForm()
        return render(
            req,
            "change.html",
            {
                "form": form,
                "title": "新建靓号",
                "req": req,
            },
        )
    form = liangModelForm(data=req.POST)
    if form.is_valid():
        form.save()
        return redirect("/liang/list/")
    return render(
        req,
        "change.html",
        {
            "form": form,
            "title": "新建靓号",
            "req": req,
        },
    )

# 编辑靓号


def liang_edit(req):
    i = req.GET.get("nid")
    # print(i)
    if req.method == "GET":
        liang = models.Liang.objects.filter(id=i).first()
        # print(liang)
        form = liangModelForm(instance=liang)
        return render(
            req,
            "change.html",
            {
                "form": form,
                "title": "编辑靓号",
                "req": req,
            },
        )
    liang = models.Liang.objects.filter(id=i).first()
    form = liangModelForm(data=req.POST, instance=liang)
    if form.is_valid():
        form.save()
        return redirect("/liang/list/")
    return render(
        req,
        "change.html",
        {
            "form": form,
            "title": "编辑靓号",
            "req": req,
        },
    )


# 删除靓号
def liang_delete(req):
    i = req.GET.get("nid")
    models.Liang.objects.filter(id=i).delete()
    return redirect("/liang/list/")
