# Generated by Django 3.0.6 on 2020-06-26 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20200625_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='timestamp_completed',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
