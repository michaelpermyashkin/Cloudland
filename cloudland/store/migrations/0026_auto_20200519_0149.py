# Generated by Django 3.0.5 on 2020-05-19 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_auto_20200519_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(help_text='Upload product image', upload_to='store/static/store/media/products/'),
        ),
    ]
