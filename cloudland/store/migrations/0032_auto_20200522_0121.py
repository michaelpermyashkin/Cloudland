# Generated by Django 3.0.5 on 2020-05-22 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_seller_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description_full',
            field=models.TextField(default='', help_text='Your full item description when item details are viewed', max_length=1000),
        ),
    ]
