# 联通后台管理系统

在B站上观看视频写的一个基于Django的后台管理系统

Django v4.1.2

[B站视频](https://www.bilibili.com/video/BV1NL41157ph?p=1&vd_source=6e7590efd0665a54e4845faba48bdb57)



### 项目启动

```
python manage.py runserver
```



### 注意

在项目启动之前要对django_deno1/django_demo1/settings.py文件中的DATABASES项进行重新配置



### 问题

> django.db.utils.NotSupportedError: MySQL 5.7 or later is required (found 5.5.40)

找到lib/python3.11/site-packages/django/db/backends/base/base.py下的self.check_database_version_supported()  ,然后注释掉，最后还是有报错，但是我改了后运行起来了

最好的解决方法应该是升级MySQL或降低Django版本