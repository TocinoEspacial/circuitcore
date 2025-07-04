# Generated by Django 5.2.2 on 2025-06-11 23:42

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ygv', '0007_alter_cotizacion_descuento_alter_cotizacion_iva_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='descuento',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=60),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='iva',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=60),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=60),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='total',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=60),
        ),
    ]
