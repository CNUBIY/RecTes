# Generated by Django 5.0.6 on 2024-06-24 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Historiales', '0007_remove_patient_num_madrecita_cell_madrecita_tf_casa_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='madrecita',
            name='cell',
        ),
        migrations.RemoveField(
            model_name='madrecita',
            name='tf_casa',
        ),
        migrations.RemoveField(
            model_name='madrecita',
            name='tf_tra',
        ),
        migrations.AddField(
            model_name='patient',
            name='cell',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='tf_casa',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='tf_tra',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
