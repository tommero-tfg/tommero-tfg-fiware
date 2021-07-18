import uuid

from django.contrib.auth.models import User
from django.db import models
from colorfield.fields import ColorField


class CarModel(models.Model):
    class Meta:
        verbose_name = 'CarModel'

    FUEL_CHOICES = [
        ('G', 'Gasolina'),
        ('D', 'Diesel'),
        ('E', 'Eléctrico'),
        ('H', 'Híbrido')
    ]
    TRANSMISSION_CHOICES = [
        ('A', 'Automático'),
        ('M', 'Manual')
    ]

    id = models.AutoField(primary_key=True)
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    name = models.CharField(max_length=64, null=False, blank=False, verbose_name='Nombre del modelo del coche')
    brand = models.CharField(max_length=64, null=False, blank=False, verbose_name='Marca del coche')
    fuel = models.CharField(max_length=1, null=True, choices=FUEL_CHOICES, default='G', verbose_name='Combustible')
    transmission = models.CharField(max_length=1, null=True, choices=TRANSMISSION_CHOICES, default='A',
                                    verbose_name='Transmisión')
    motor = models.IntegerField(null=True, verbose_name='Potencia del coche')
    seats = models.IntegerField(null=True, verbose_name='Número de puertas del coche')
    average_consumption = models.FloatField(null=True, verbose_name='Consumo medio del coche a los 100L')
    price = models.IntegerField(null=True, verbose_name='Precio anual del coche')
    release_year = models.CharField(max_length=4, null=True, blank=True, verbose_name='Fecha de estreno')

    creation_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                             verbose_name='Fecha de creación')
    modification_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                                 verbose_name='Fecha de modificación')

    def __str__(self):
        return f'{self.name}'

    @property
    def base_price(self):
        return self.price // 70


class ModelReview(models.Model):
    id = models.AutoField(primary_key=True)
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    text = models.CharField(max_length=128, null=True, verbose_name='Texto de la descripción')

    user = models.ForeignKey(User, null=False, blank=False, related_name='reviews', on_delete=models.CASCADE,
                             verbose_name='Usuario de la reseña')
    car = models.ForeignKey(CarModel, null=False, blank=False, related_name='reviews', on_delete=models.CASCADE,
                            verbose_name='Modelo de la reseña')

    creation_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                             verbose_name='Fecha de creación')
    modification_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                                 verbose_name='Fecha de modificación')

    def __str__(self):
        return f'Reseña de {self.user.username} al modelo {self.car.name}'


class CarImage(models.Model):
    id = models.AutoField(primary_key=True)
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    name = models.CharField(max_length=64, null=True, blank=True, verbose_name='Nombre del color')
    color = ColorField(max_length=64, null=False, blank=False, verbose_name='color en hex')
    image = models.ImageField(upload_to='carmodels', null=True, verbose_name='Imagen del modelo')

    car = models.ForeignKey(CarModel, null=True, blank=True, related_name='images', on_delete=models.CASCADE,
                            verbose_name='Coche asociado a esta imagen')

    creation_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                             verbose_name='Fecha de creación')
    modification_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                                 verbose_name='Fecha de modificación')

    def __str__(self):
        return f'Color {self.color} del coche'
