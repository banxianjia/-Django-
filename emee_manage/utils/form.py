

from pyexpat import model
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, HttpResponse, redirect


from emee_manage import models
from emee_manage.utils.bootstrap import BootStrapModelForm, BootStrapForm
from emee_manage.utils.encrypt import md5


class UploadModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = "__all__"



class UploadForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")

class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid","admin"]

class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"

class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = "__all__"

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        confirm = md5(self.cleaned_data.get("confirm_password"))
        password = self.cleaned_data.get("password")
        if confirm != password:
            raise ValidationError("密码不一致")
        return confirm


class DepartModelForm(BootStrapModelForm):
    class Meta:
        model = models.Department
        fields = ["depart"]


class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "salary",
                  "creat_time", "depart", "gender"]
        # widgets = {
        #     "name":forms.TextInput(attrs={"class":"form-control"}),
        #     "password":forms.TextInput(attrs={"class":"form-control"}),
        #     "age":forms.NumberInput(attrs={"class":"form-control"}),
        #     "salary":forms.NumberInput(attrs={"class":"form-control"}),
        #     "creat_time":forms.DateTimeInput(attrs={"class":"form-control"}),
        # }


class liangModelForm(BootStrapModelForm):
    # 验证方式一
    mobile = forms.CharField(
        label="号码",
        validators=[RegexValidator(r'^159\d{8}$', '号码格式错误,数字必须以159开头')]

    )

    class Meta:
        model = models.Liang
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"
        # exclude = [] 除了

    # 验证 方式二 钩子方法
    # def clean_mobile(self):
    #     pr_mobile = self.cleaned_data['mobile']
        # if len(pr_mobile) != 11 & models.Liang.objects.filter(mobile=pr_mobile).exists():
        #         raise ValidationError("号码格式错误")

        #     return pr_mobile
