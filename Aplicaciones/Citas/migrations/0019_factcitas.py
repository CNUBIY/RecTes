# Generated by Django 4.2.7 on 2024-06-04 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0018_citasol_telf_da'),
    ]

    operations = [
        migrations.CreateModel(
            name='FactCitas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idfac', models.CharField(max_length=150)),
                ('descfac', models.CharField(max_length=150)),
                ('valfac', models.DecimalField(decimal_places=2, max_digits=5)),
                ('obsfac', models.CharField(max_length=150)),
                ('fechfac', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Citas.citasol')),
            ],
        ),
    ]
