# Generated by Django 3.0.6 on 2020-05-29 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200529_0559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailconfirmed',
            old_name='activations_key',
            new_name='activation_key',
        ),
    ]
