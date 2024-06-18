# Generated by Django 5.0.6 on 2024-06-15 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresarial', '0011_empleado_salario_alter_empleado_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculos',
            name='dias_vacaciones',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='calculos',
            name='icbf',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='calculos',
            name='sena',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='calculos',
            name='transporte',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='estado_u',
            field=models.BooleanField(default=False),
        ),
    ]
