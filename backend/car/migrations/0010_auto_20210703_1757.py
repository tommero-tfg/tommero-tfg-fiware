# Generated by Django 2.2.19 on 2021-07-03 17:57

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0009_carimage_car'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carmodel',
            name='colors',
        ),
        migrations.RemoveField(
            model_name='carmodel',
            name='image',
        ),
        migrations.AddField(
            model_name='carimage',
            name='name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Nombre del color'),
        ),
        migrations.AlterField(
            model_name='carimage',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', max_length=64, verbose_name='color en hex'),
        ),
        migrations.DeleteModel(
            name='CarColor',
        ),
    ]
