from openpyxl import load_workbook

from django.shortcuts import render, HttpResponse, redirect

from emee_manage import models
from emee_manage.utils.form import DepartModelForm



def depart_list(req):
    depart = models.Department.objects.all()
    print(depart)
    return render(
        req,
        "depart_list.html",
        {
            "depart": depart,
            "req": req,
        },
    )

def depart_mult(req):
    file_object = req.FILES.get("file")
    wb = load_workbook(file_object)
    sheet = wb.worksheets[0]
    # 利用openpyxl对excel进行操作获取相关数据，再利用models存入数据库
    return HttpResponse("上传文件")

def depart_add(req):
    if req.method == "GET":
        return render(
            req,
            "depart_add.html",
        )
    title = req.POST.get("title")
    models.Department.objects.create(depart=title)
    return redirect("/depart/list/")


def depart_add_modelform(req):
    if req.method == "GET":
        form = DepartModelForm()
        return render(
            req,
            "change.html",
            {
                "form": form,
                "title": "新建部门",
                "req": req,
            },
        )
    form = DepartModelForm(data=req.POST)
    if form.is_valid():
        form.save()
        return redirect("/depart/list/")
    return render(
        req,
        "change.html",
        {
            "form": form,
            "title": "新建部门",
            "req": req,
        },
    )

# 编辑部门


def depart_edit(req):
    i = req.GET.get("nid")
    if req.method == "GET":

        obj = models.Department.objects.filter(id=i).first()
        return render(
            req,
            "depart_edit.html",
            {
                "obj": obj,
                "req": req,
            },
        )
    title = req.POST.get("title")
    models.Department.objects.filter(id=i).update(depart=title)
    return redirect("/depart/list/")

# 删除部门


def depart_delete(req):
    i = req.GET.get("nid")
    models.Department.objects.filter(id=i).delete()
    return redirect("/depart/list/")
