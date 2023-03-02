from pyexpat import model
from django.shortcuts import render, HttpResponse, redirect

from emee_manage import models
from emee_manage.utils.pagination import Pagination
from emee_manage.utils.form import AdminModelForm
from emee_manage.utils.encrypt import md5


def admin_list(req):
    search_value = req.GET.get("q", "")
    data_dict = {}
    if search_value:
        data_dict["username__contains"] = search_value

    queryset = models.Admin.objects.filter(**data_dict)
    page_manage = Pagination(req, queryset)
    return render(
        req,
        "admin_list.html",
        {
            "search_value": search_value,
            "queryset": page_manage.page_queryset,
            "page_str": page_manage.html(),
            "req": req,
        },

    )


def admin_add(req):
    if req.method == "GET":
        form = AdminModelForm()
        return render(
            req,
            "change.html",
            {
                "form": form,
                "title": "管理员",
                "req": req,
            },
        )
    form = AdminModelForm(data=req.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(
        req,
        "change.html",
        {
            "form": form,
            "title": "管理员",
            "req": req,
        },
    )


def admin_edit(req):
    i = req.GET.get("nid")
    admin = models.Admin.objects.filter(id=i).first()
    if not admin:
        return redirect("/admin/list/")
    if req.method == "GET":
        form = AdminModelForm()
        return render(
            req,
            "change.html",
            {
                "form": form,
                "title": "编辑管理员",
                "req": req,
            }
        )
    form = AdminModelForm(data=req.POST, instance=admin)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(
        req,
        "change.html",
        {
            "form": form,
            "title": "编辑管理员",
            "req": req,
        }
    )


def admin_delete(req):
    i = req.GET.get("nid")
    models.Admin.objects.filter(id=i).delete()
    return redirect("/admin/list")


def admin_reset(req):
    i = req.GET.get("nid")
    pwd = md5("123456")
    models.Admin.objects.filter(id=i).update(password=pwd)
    return redirect("/admin/list")
