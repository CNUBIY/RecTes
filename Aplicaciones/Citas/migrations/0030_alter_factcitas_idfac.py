# Generated by Django 5.0.6 on 2024-08-01 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0029_solcli_agendado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factcitas',
            name='idfac',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
