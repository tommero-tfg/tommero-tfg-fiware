# Generated by Django 2.2.19 on 2021-07-03 16:39

import colorfield.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0006_auto_20210703_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', max_length=64, verbose_name='Nombre del color en castellano')),
                ('image', models.ImageField(null=True, upload_to='carmodels', verbose_name='Imagen del modelo')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modification_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de modificación')),
            ],
        ),
        migrations.AddField(
            model_name='carmodel',
            name='release_year',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Fecha de estreno'),
        ),
        migrations.AlterField(
            model_name='carmodel',
            name='fuel',
            field=models.CharField(choices=[('G', 'Gasolina'), ('D', 'Diesel'), ('E', 'Eléctrico'), ('H', 'Híbrido')], default='G', max_length=1, null=True, verbose_name='Combustible'),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='images',
            field=models.ManyToManyField(related_name='cars', to='car.CarImage'),
        ),
    ]
