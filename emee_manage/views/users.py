
from gettext import install
from dataclasses import fields
from turtle import title
from django.shortcuts import render, HttpResponse, redirect
from emee_manage import models
from emee_manage.utils.pagination import Pagination
from emee_manage.utils.form import UserModelForm
# 用户列表


def users_list(req):
    users = models.UserInfo.objects.all()
    # for obj in users:
    #     print(
    #         obj.creat_time.strftime("%Y-%m-%d"),
    #         obj.get_gender_display()
    #     )
    users_pagination = Pagination(req, users, page_size=2)
    return render(
        req,
        "users_list.html",
        {
            "users_queryset": users_pagination.page_queryset,
            "users_str": users_pagination.html(),
            "req": req,
        },
    )

# 新建用户


def users_add(req):
    if req.method == "GET":

        return render(
            req,
            "users_add.html",
            {
                'gender_choices': models.UserInfo.gender_choices,
                'depart_list': models.Department.objects.all(),
                "req": req,
            }
        )
    user = req.POST.get("user")
    pwd = req.POST.get("pwd")
    age = req.POST.get("age")
    sa = req.POST.get("sa")
    ctime = req.POST.get("ctime")
    db = req.POST.get("db")
    sex = req.POST.get("sex")
    models.UserInfo.objects.create(
        name=user,
        password=pwd,
        age=age,
        salary=sa,
        creat_time=ctime,
        depart_id=db,
        gender=sex)
    return redirect("/users/list/")

# 编辑用户


def users_edit(req):
    i = req.GET.get("nid")
    if req.method == "GET":
        u = models.UserInfo.objects.filter(id=i).first()
        gender_choices = models.UserInfo.gender_choices
        depart_list = models.Department.objects.all()
        return render(
            req,
            "users_edit.html",
            {
                "user": u,
                "gender_choices": gender_choices,
                "depart_list": depart_list,
                "req": req,
            },
        )
    user = req.POST.get("user")
    pwd = req.POST.get("pwd")
    age = req.POST.get("age")
    sa = req.POST.get("sa")
    ctime = req.POST.get("ctime")
    db = req.POST.get("db")
    sex = req.POST.get("sex")
    models.UserInfo.objects.filter(id=i).update(
        name=user,
        password=pwd,
        age=age,
        salary=sa,
        creat_time=ctime,
        depart_id=db,
        gender=sex)
    return redirect("/users/list/")


# 删除用户


def users_delete(req):
    i = req.GET.get("nid")
    models.UserInfo.objects.filter(id=i).delete()
    return redirect("/users/list/")


def users_add_modelform(req):
    if req.method == "GET":
        form = UserModelForm()
        return render(
            req,
            "change.html",
            {
                "form": form,
                "title": "新建用户",
                "req": req,
            }
        )

    form = UserModelForm(data=req.POST)
    if form.is_valid():
        form.save()
        # form.cleaned_data
        return redirect("/users/list/")
    return render(
        req,
        "change.html",
        {
            "form": form,
            "title": "新建用户",
            "req": req,
        }
    )
