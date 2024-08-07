# Generated by Django 5.0.6 on 2024-06-02 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0014_representantecita_delete_representante'),
    ]

    operations = [
        migrations.CreateModel(
            name='CitaSol',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fech_da', models.DateField()),
                ('time_da', models.TimeField()),
            ],
        ),
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
        migrations.DeleteModel(
            name='RepresentanteCita',
        ),
    ]
