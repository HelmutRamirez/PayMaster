# Generated by Django 5.0.6 on 2024-06-14 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Independientes', '0009_passwordresetrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordresetrequest',
            name='expires_at',
            field=models.DateTimeField(null=True),
        ),
    ]