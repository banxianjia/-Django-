from email.policy import default
from operator import length_hint
from random import choices
from statistics import mode
from sys import maxsize
from tabnanny import verbose
from turtle import title
from django.db import models

# Create your models here.


class Department(models.Model):
    """部门表"""
    depart = models.CharField(verbose_name="部门名称", max_length=32)

    def __str__(self):
        return self.depart


class UserInfo(models.Model):
    """用户表"""
    # id bigint auto_increment primary key
    name = models.CharField(verbose_name="姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    salary = models.DecimalField(
        verbose_name="薪水", max_digits=10, decimal_places=2, default=0)
    creat_time = models.DateTimeField(verbose_name="入职时间")

    # 有约束字段
    # - to,与哪张表关联
    # - to_field,与哪字段关联
    # django自动生成数据列  depart_id
    # 联级删除  on_delete=models.CASCADE
    # 置空 null=true,blank=true,on_delete=models.SET_NULL
    depart = models.ForeignKey(
        verbose_name="所属部门", to="Department", to_field="id", on_delete=models.CASCADE, null=True, blank=True)

    # django约束  choices
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(
        verbose_name="性别", choices=gender_choices)


class Liang(models.Model):
    """"靓号表"""

    mobile = models.CharField(verbose_name="号码", max_length=11)  # 定长
    price = models.IntegerField(verbose_name="价格")
    level_choices = (
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
        (4, "四级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices)
    status_choice = (
        (1, "已使用"),
        (2, "未使用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choice)


class Admin(models.Model):
    """管理员表"""
    username = models.CharField(verbose_name="昵称", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)

    def __str__(self):
        return self.username

class Task(models.Model):
    """任务表"""
    level_choices = (
        (1,"紧急"),
        (2,"一般"),
        (3,"普通")
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)

class Order(models.Model):
    """订单表"""
    oid = models.CharField(verbose_name="订单号", max_length=32)
    goods_name = models.CharField(verbose_name="商品名称",max_length=64)
    price = models.IntegerField(verbose_name="价格")
    status_choices = (
        (1,"待支付"),
        (2,"已支付")
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices,default=1)
    admin = models.ForeignKey(verbose_name="用户",to="Admin", to_field="id", on_delete=models.CASCADE)

class Boss(models.Model):
    """老板表"""
    name = models.CharField(verbose_name="姓名",max_length=64)
    age = models.IntegerField(verbose_name="年龄",max_length=32)
    img = models.CharField(verbose_name="头像路径",max_length=128)

class City(models.Model):
    """城市表"""
    name = models.CharField(verbose_name="名称",max_length=64)
    count = models.IntegerField(verbose_name="人口",max_length=32)
    # 本质上数据库存的还是CharField,自动保存到media/[upload_to]
    img = models.FileField(verbose_name="Logo",max_length=128, upload_to="city/")