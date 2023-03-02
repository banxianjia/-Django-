from io import BytesIO

from django.shortcuts import render, HttpResponse, redirect

from emee_manage import models
from emee_manage.utils.encrypt import md5
from emee_manage.utils.code import check_code


def login(req):
    if req.method == "GET":
        return render(
            req,
            "login.html",
        )
    username = req.POST.get("username")
    pwd = md5(req.POST.get("password"))
    input_code = req.POST.get("code")
    print(username, pwd)
    flag = models.Admin.objects.filter(
        username=username, password=pwd).exists()
    code_str = req.session.get('image_code', "")
    print(input_code+'==?'+code_str)
    if not code_str:
        msg = "验证码超时"
    elif input_code != code_str:
        msg = "验证码错误"
    elif flag:
        req.session["info"] = {
                "id":models.Admin.objects.filter(username=username).first().id,
                "name":username
            }
        req.session.set_expiry(60*60*24)
        return redirect("/admin/list/")
    else:
        msg = "账号或密码错误"
    return render(
        req,
        "login.html",
        {
            "msg": msg,
        }
    )


def logout(req):
    req.session.clear()
    return redirect("/login/")


def image_code(req):
    img, code_str = check_code()
    # 将code_str存入session中
    req.session['image_code'] = code_str
    # 设置有效时间
    req.session.set_expiry(60)
    # 写入内存(Python3)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
