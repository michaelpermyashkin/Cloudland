# Generated by Django 3.0.5 on 2020-05-19 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_auto_20200519_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(help_text='Upload product image', upload_to='product_images'),
        ),
    ]
