# Generated by Django 2.2.2 on 2019-07-16 07:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190716_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogarticles',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间'),
        ),
        migrations.AlterField(
            model_name='blogarticles',
            name='title',
            field=models.CharField(max_length=300, verbose_name='标题'),
        ),
    ]
