# Generated by Django 5.2.2 on 2025-06-18 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ygv', '0014_alter_cotizacion_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacionitem',
            name='unidad_medida',
            field=models.CharField(choices=[('M2', 'Metros cuadrados (m²)'), ('ML', 'Metros lineales (ml)'), ('M3', 'Metros cúbicos (m³)'), ('UNIDAD', 'Unidad(es)'), ('HORA', 'Hora(s) de trabajo'), ('DIA', 'Día(s) de trabajo'), ('GALON', 'Galón(es)'), ('KG', 'Kilogramo(s)'), ('LITRO', 'Litro(s)')], default='UNIDAD', max_length=10, verbose_name='Unidad de medida'),
        ),
    ]
