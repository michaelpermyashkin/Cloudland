# Generated by Django 3.0.5 on 2020-04-16 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20200416_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productName',
            field=models.CharField(max_length=25),
        ),
    ]
