# Generated by Django 4.2.7 on 2024-05-28 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0010_remove_usuariocli_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariocli',
            name='telf_us',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
