# Generated by Django 5.0.6 on 2024-06-12 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresarial', '0006_empresa_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='id_rol',
            field=models.CharField(choices=[('Contador', 'Contador'), ('Auxiliar Contable', 'Auxiliar Contable'), ('RRHH', 'RRHH'), ('Empleado General', 'Empleado General')], max_length=30),
        ),
    ]
