# Generated by Django 2.2.19 on 2021-06-13 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0002_auto_20210613_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='image',
            field=models.ImageField(null=True, upload_to='carmodels', verbose_name='Imagen del modelo'),
        ),
    ]
