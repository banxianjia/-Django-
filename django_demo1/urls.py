"""django_demo1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# 项目的 URL 声明，就像你网站的“目录”

from django.conf import settings
from django.urls import path,re_path
from django.views.static import serve

from emee_manage.views import depart, users, liang, admin, account, task, order, chart, upload

urlpatterns = [
    # path('admin/', admin.site.urls),

    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT},name='media'),

    # 首页
    path('login/', account.login),
    path("logout/", account.logout),
    path("image/code/", account.image_code),

    # 部门
    path("depart/list/", depart.depart_list),
    path("depart/mult/", depart.depart_mult),
    path("depart/add/", depart.depart_add),
    path("depart/add_modelform/", depart.depart_add_modelform),
    path("depart/edit/", depart.depart_edit),
    path("depart/delete/", depart.depart_delete),


    # 用户
    path("users/list/", users.users_list),
    path("users/add/", users.users_add),
    path("users/add_modelform/", users.users_add_modelform),
    path("users/edit/", users.users_edit),
    path("users/delete/", users.users_delete),


    # 靓号
    path("liang/list/", liang.liang_list),
    path("liang/add/", liang.liang_add),
    path("liang/edit/", liang.liang_edit),
    path("liang/delete/", liang.liang_delete),


    # 管理员
    path("admin/list/", admin.admin_list),
    path("admin/add/", admin.admin_add),
    path("admin/edit/", admin.admin_edit),
    path("admin/delete/", admin.admin_delete),
    path("admin/reset/", admin.admin_reset),

    # 任务管理
    path("task/list/", task.task_list),
    path("task/ajax/", task.task_ajax),
    path("task/add/", task.task_add),
    path("task/delete/",task.task_delete),
    path("task/edit/",task.task_edit),

    #订单管理
    path("order/list/",order.order_list),
    path("order/add/",order.order_add),
    path("order/delete/",order.order_delete),
    path("order/edit/",order.order_edit),

    # 数据统计
    path("chart/list/",chart.chart_list),

    # form上传
    path("upload/form/",upload.upload_form),
    path("upload/model/form/",upload.upload_modelform),
    path("city/list/",upload.upload_list),
    path("city/edit/",upload.city_edit),
    path("city/delete/",upload.city_delete)
]
