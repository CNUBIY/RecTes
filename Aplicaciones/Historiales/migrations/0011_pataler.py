# Generated by Django 5.0.7 on 2024-07-17 19:10

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Historiales', '0010_alergia'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatAler',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation', models.DateField(default=datetime.date.today)),
                ('alergia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Historiales.alergia')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Historiales.patient')),
            ],
        ),
    ]
