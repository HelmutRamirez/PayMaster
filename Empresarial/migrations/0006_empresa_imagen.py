# Generated by Django 5.0.6 on 2024-06-07 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresarial', '0005_empleado_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='imagen',
            field=models.ImageField(default='', upload_to='photos'),
            preserve_default=False,
        ),
    ]
