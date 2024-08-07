# Generated by Django 4.2.7 on 2024-04-09 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0003_diahorario'),
    ]

    operations = [
        migrations.CreateModel(
            name='HorasDia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('horaInicio', models.TimeField()),
                ('horaFinal', models.TimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='diahorario',
            name='horaFInal',
        ),
        migrations.RemoveField(
            model_name='diahorario',
            name='horaInicio',
        ),
        migrations.AddField(
            model_name='diahorario',
            name='horario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Citas.horasdia'),
        ),
    ]
