# Generated by Django 5.0.6 on 2024-06-11 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Historiales', '0003_remove_patient_creation'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='creation',
            field=models.DateField(blank=True, null=True),
        ),
    ]