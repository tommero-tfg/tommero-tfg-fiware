# Generated by Django 2.2.19 on 2021-06-13 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarColor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Nombre del color')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modification_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de modificación')),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Nombre del modelo del coche')),
                ('brand', models.CharField(max_length=64, verbose_name='Marca del coche')),
                ('description', models.CharField(max_length=128, null=True, verbose_name='Descripción del coche')),
                ('fuel', models.CharField(choices=[('G', 'Gasolina'), ('D', 'Diesel')], default='G', max_length=1, null=True, verbose_name='Combustible')),
                ('transmission', models.CharField(choices=[('A', 'Automático'), ('M', 'Manual')], default='A', max_length=1, null=True, verbose_name='Transmisión')),
                ('motor', models.IntegerField(null=True, verbose_name='Potencia del coche')),
                ('seats', models.IntegerField(null=True, verbose_name='Número de puertas del coche')),
                ('average_consumption', models.IntegerField(null=True, verbose_name='Consumo medio del coche a los 100L')),
                ('price', models.IntegerField(null=True, verbose_name='Precio anual del coche')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modification_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de modificación')),
                ('colors', models.ManyToManyField(related_name='cars', to='car.CarColor')),
            ],
        ),
    ]
