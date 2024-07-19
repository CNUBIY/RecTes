# Generated by Django 5.0.6 on 2024-07-18 05:53

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Historiales', '0012_infomom'),
    ]

    operations = [
        migrations.CreateModel(
            name='observaciones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation', models.DateField(default=datetime.date.today)),
                ('new_age', models.CharField(max_length=250)),
                ('firstsect', models.TextField()),
                ('secondsect', models.TextField()),
                ('cortesia', models.BooleanField(default=False)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Historiales.patient')),
            ],
        ),
    ]