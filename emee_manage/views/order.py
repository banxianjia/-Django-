from distutils.log import error
import json
import random
from datetime import datetime
from sys import flags
from django.urls import is_valid_path
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect,HttpResponse

from emee_manage import models
from emee_manage.utils.form import OrderModelForm

def order_list(req):
    order_queryset = models.Order.objects.all().order_by('id')
    form = OrderModelForm()
    return render(
        req,
        "order_list.html",
        {
            "req":req,
            "form":form,
            "order_queryset":order_queryset,
        }
    )
@csrf_exempt
def order_add(req):
    form = OrderModelForm(data=req.POST)
    print(req.POST)
    if form.is_valid():
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S")+str(random.randint(1000,9999))
        form.instance.admin_id = req.session["info"]["id"]
        form.save()
        data_dict = {
            "status": True,
        }
        return HttpResponse(json.dumps(data_dict))
    data_dict = {
        "status": False,
        "error": form.errors,
    }
    return HttpResponse(json.dumps(data_dict))

def order_delete(req):
    i = req.GET.get("nid")
    if not models.Order.objects.filter(id=i).exists():
        data_dict = {
            "status":False,
            "error": "删除失败，数据不存在。"
        }
        return HttpResponse(json.dumps(data_dict))
    models.Order.objects.filter(id=i).delete()
    data_dict = {
        "status": True,
    }
    return HttpResponse(json.dumps(data_dict))

@csrf_exempt
def order_edit(req):
    i = req.GET.get("nid")
    flag= models.Order.objects.filter(id=i).exists()
    if req.method == "GET":
        if not flag:
            return HttpResponse(json.dumps({"status":False,"error":"编辑失败，数据不存在。"}))
        data_dict ={
            "status":True,
            "data":models.Order.objects.filter(id=i).values("goods_name","price","status").first()
        }
        return HttpResponse(json.dumps(data_dict))
    print(req.POST)
    order = models.Order.objects.filter(id=i).first()
    form = OrderModelForm(data=req.POST,instance=order)
    if form.is_valid():
        form.save()
        return HttpResponse(json.dumps({"status":True}))
    return HttpResponse(json.dumps({"status":False,"error": form.errors}))