# Generated by Django 3.0.6 on 2020-06-03 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200603_0150'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraddress',
            old_name='is_shipping',
            new_name='shipping',
        ),
    ]