import json

from django.shortcuts import redirect, render, HttpResponse
from django.urls import is_valid_path
from django.views.decorators.csrf import csrf_exempt
from emee_manage import models
from emee_manage.utils.form import TaskModelForm

def task_list(req):
    task_queryset = models.Task.objects.all().order_by('-id')

    form = TaskModelForm()
    return render(
        req,
        "task_list.html",
        {
            "req": req,
            "form":form,
            "task_queryset":task_queryset,
        }
    )

def task_delete(req):
    i = req.GET.get("nid")
    models.Task.objects.filter(id=i).delete()
    return redirect("/task/list/")

def task_edit(req):
    i = req.GET.get("nid")
    task = models.Task.objects.filter(id=i).first()
    if req.method == "GET":
        form = TaskModelForm(instance=task)
        return render(
            req,
            "change.html",
            {
                "form":form,
                "title":"编辑任务",
                "req":req,
            }
        )
    form = TaskModelForm(data=req.POST,instance=task)
    if form.is_valid():
        form.save()
        return redirect("/task/list/")
    return render(
        req,
        "change.html",
        {
            "form":form,
            "title":"编辑任务",
            "req":req,
        }
    )

@csrf_exempt
def task_ajax(req):
    data_dict = {
        "status": True,
        'data': [11, 22, 33, 44],
    }
    return HttpResponse(json.dumps(data_dict))

@csrf_exempt
def task_add(req):
    form = TaskModelForm(data = req.POST)
    if form.is_valid():
        form.save()
        data_dict = {
            "status": True,
        }
        return HttpResponse(json.dumps(data_dict))
    data_dict = {
        "status": False,
        "error": form.errors
    }
    return HttpResponse(json.dumps(data_dict))
