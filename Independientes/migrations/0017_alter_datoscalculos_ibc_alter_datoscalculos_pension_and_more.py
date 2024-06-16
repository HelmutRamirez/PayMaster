# Generated by Django 5.0.6 on 2024-06-16 19:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Independientes', '0016_alter_datoscalculos_ibc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datoscalculos',
            name='ibc',
            field=models.FloatField(null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(40)]),
        ),
        migrations.AlterField(
            model_name='datoscalculos',
            name='pension',
            field=models.FloatField(default=16, max_length=50),
        ),
        migrations.AlterField(
            model_name='datoscalculos',
            name='salud',
            field=models.FloatField(default=12.5, max_length=50),
        ),
    ]
