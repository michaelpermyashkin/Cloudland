# Generated by Django 3.0.6 on 2020-06-20 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0009_cart_shipping'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='grand_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]