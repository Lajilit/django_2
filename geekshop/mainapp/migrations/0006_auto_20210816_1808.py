# Generated by Django 3.2.5 on 2021-08-16 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20210618_0017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='is_deleted',
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='товар активен'),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='категория активна'),
        ),
    ]
