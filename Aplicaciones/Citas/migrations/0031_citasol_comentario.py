# Generated by Django 5.0.6 on 2024-08-06 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0030_alter_factcitas_idfac'),
    ]

    operations = [
        migrations.AddField(
            model_name='citasol',
            name='comentario',
            field=models.TextField(blank=True, null=True),
        ),
    ]