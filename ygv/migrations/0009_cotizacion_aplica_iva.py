# Generated by Django 5.2.2 on 2025-06-11 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ygv', '0008_alter_cotizacion_descuento_alter_cotizacion_iva_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizacion',
            name='aplica_iva',
            field=models.BooleanField(default=True),
        ),
    ]
