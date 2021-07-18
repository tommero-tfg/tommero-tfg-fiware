# Generated by Django 2.2.19 on 2021-06-13 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carcolor',
            name='name',
        ),
        migrations.AddField(
            model_name='carcolor',
            name='name_en',
            field=models.CharField(default='red', max_length=64, verbose_name='Nombre del color en inglés'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carcolor',
            name='name_es',
            field=models.CharField(default='red', max_length=64, verbose_name='Nombre del color en castellano'),
            preserve_default=False,
        ),
    ]
