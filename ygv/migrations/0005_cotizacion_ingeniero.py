# Generated by Django 5.2.2 on 2025-06-11 22:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ygv', '0004_alter_cotizacion_administrador'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizacion',
            name='ingeniero',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cotizaciones_aprobadas', to=settings.AUTH_USER_MODEL),
        ),
    ]
