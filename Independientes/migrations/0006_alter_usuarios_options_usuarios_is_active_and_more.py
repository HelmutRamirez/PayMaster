# Generated by Django 5.0.6 on 2024-06-13 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Independientes', '0005_usuarios_documento'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuarios',
            options={},
        ),
        migrations.AddField(
            model_name='usuarios',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usuarios',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
