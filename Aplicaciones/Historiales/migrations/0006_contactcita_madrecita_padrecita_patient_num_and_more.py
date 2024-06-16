# Generated by Django 5.0.6 on 2024-06-16 22:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Historiales', '0005_alter_patient_creation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactCita',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tf_casa', models.CharField(max_length=150)),
                ('cell', models.CharField(max_length=150)),
                ('tf_tra', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='MadreCita',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom_mom', models.CharField(max_length=150)),
                ('ape_mom', models.CharField(max_length=150)),
                ('age_mom', models.DateField()),
                ('hij_mom', models.IntegerField()),
                ('es_cimom', models.CharField(max_length=150)),
                ('act_mom', models.CharField(max_length=150)),
                ('correo_mom', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='PadreCita',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom_fat', models.CharField(max_length=150)),
                ('ape_fat', models.CharField(max_length=150)),
                ('age_fat', models.DateField()),
                ('act_fat', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='num',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Historiales.contactcita'),
        ),
        migrations.AddField(
            model_name='patient',
            name='mom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Historiales.madrecita'),
        ),
        migrations.AddField(
            model_name='patient',
            name='dad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Historiales.padrecita'),
        ),
    ]
