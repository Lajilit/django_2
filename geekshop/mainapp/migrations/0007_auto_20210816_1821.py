# Generated by Django 3.2.5 on 2021-08-16 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20210816_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='товар активен'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='категория активна'),
        ),
    ]
