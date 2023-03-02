import os

from django.conf import settings
from django.shortcuts import redirect, render, HttpResponse

from emee_manage import models
from emee_manage.utils.form import UploadForm,UploadModelForm

def upload_form(req):
    if req.method == "GET":
        form = UploadForm()
        return render(
            req,
            "upload_form.html",
            {
                "title": "Form上传",
                "form":form,
                "req":req,
            }
        )
    form = UploadForm(data=req.POST,files=req.FILES)
    if form.is_valid():
        img_obj = form.cleaned_data.get("img")
        print(type(img_obj))
        db_img_path = os.path.join("static","img",img_obj.name)
        img_path = os.path.join("emee_manage",db_img_path)
        f = open(img_path,mode="wb")
        for chunk in img_obj.chunks():
            f.write(chunk)
        f.close()
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=db_img_path
        )
        return HttpResponse("上传成功")
    return render(
            req,
            "upload_form.html",
            {
                "title": "Form上传",
                "form":form,
                "req":req,
            }
        )

def upload_modelform(req):
    if req.method == "GET":
        form = UploadModelForm()
        return render(
            req,
            "upload_form.html",
            {
                "title":"ModelForm上传",
                "form":form,
                "req":req
            }
        )
    # print(req.FILES)
    form = UploadModelForm(data=req.POST,files=req.FILES)
    if form.is_valid():
        form.save()
        return redirect("/city/list/")
    return render(
            req,
            "upload_form.html",
            {
                "title":"ModelForm上传",
                "form":form,
                "req":req
            }
        )

def upload_list(req):
    queryset = models.City.objects.all().order_by("id")
    return render(
        req,
        "city_list.html",
        {
            "city_queryset":queryset,
            "req":req,
        }
    )

def city_edit(req):
    i = req.GET.get("nid")
    # print(i)
    if req.method == "GET":
        city = models.City.objects.filter(id=i).first()
        form = UploadModelForm(instance=city)
        return render(
            req,
            "change.html",
            {
                "form": form,
                "title": "编辑城市",
                "req": req,
            },
        )
    print(req.FILES)
    print(req.POST)
    return redirect("/city/list/")
    # city = models.City.objects.filter(id=i).first()
    # form = UploadModelForm(data=req.POST, files=req.FILES, instance=city)
    # if form.is_valid():
        # form.save()
        # return redirect("/city/list/")
    # return render(
        # req,
    #     "change.html",
    #     {
    #         "form": form,
    #         "title": "编辑城市",
    #         "req": req,
    #     },
    # )



def city_delete(req):
    i = req.GET.get("nid")
    path = models.City.objects.filter(id=i).first().img
    q_path = os.path.join(str(settings.MEDIA_ROOT),str(path))
    models.City.objects.filter(id=i).delete()
    os.remove(q_path)
    return redirect("/city/list/")