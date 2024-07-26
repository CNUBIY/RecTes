# Generated by Django 5.0.6 on 2024-07-26 01:43

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Historiales', '0022_curvas'),
    ]

    operations = [
        migrations.AddField(
            model_name='curvas',
            name='per_enc',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
