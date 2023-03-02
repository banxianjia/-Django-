# Generated by Django 2.0 on 2022-09-30 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emee_manage', '0003_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.SmallIntegerField(choices=[(1, '紧急'), (2, '一般'), (3, '普通')], default=1, verbose_name='级别')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('detail', models.TextField(verbose_name='详细信息')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emee_manage.Admin', verbose_name='负责人')),
            ],
        ),
    ]