# Generated by Django 4.2.7 on 2024-05-28 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0008_generoscli_usuariocli_gen_us'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariocli',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usuariocli',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usuariocli',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='usuariocli',
            name='password',
            field=models.CharField(default=123456, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usuariocli',
            name='correo_us',
            field=models.EmailField(max_length=150, unique=True),
        ),
    ]