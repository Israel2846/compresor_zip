# Generated by Django 5.0 on 2023-12-14 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compresor', '0003_alter_factura_rutaappfact_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='factura',
            old_name='FechaDeTimbrado',
            new_name='fecha_timbrado',
        ),
        migrations.RenameField(
            model_name='factura',
            old_name='RutaAppFact',
            new_name='ruta_app_fact',
        ),
        migrations.RenameField(
            model_name='factura',
            old_name='RutaProduccion',
            new_name='ruta_produccion',
        ),
    ]