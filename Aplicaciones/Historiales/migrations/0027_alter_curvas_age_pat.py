# Generated by Django 5.0.6 on 2024-07-29 02:56

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Historiales', '0026_alter_estaturasrep_paciente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curvas',
            name='age_pat',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
