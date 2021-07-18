import uuid

from django.db import models
from django.contrib.auth.models import User

from car.models import CarModel


class Contract(models.Model):
    STATUS_CHOICES = [
        ('E', 'En proceso'),
        ('A', 'Activo'),
        ('F', 'Finalizado'),
        ('C', 'Cancelado')
    ]

    id = models.AutoField(primary_key=True)
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    monthly_cost = models.FloatField(null=True, verbose_name='Coste mensual del contrato')
    annual_mileage = models.IntegerField(null=True, verbose_name='Kilometraje anual del contrato')
    duration = models.IntegerField(null=True, verbose_name='Duración del contrato')
    start_date = models.DateField(null=True, blank=True, verbose_name='Fecha de activación')
    reject_date = models.DateField(null=True, blank=True, verbose_name='Fecha de finalización')
    bank_account = models.CharField(max_length=64, null=False, blank=False, verbose_name='Número de cuenta bancaria')
    status = models.CharField(max_length=1, null=False, choices=STATUS_CHOICES, default='E', verbose_name='Estado')
    car_color = models.CharField(max_length=30, null=False, blank=False, verbose_name='Color del modelo del coche')
    document = models.FileField(upload_to='contracts/', null=True, blank=True)

    user = models.ForeignKey(User, null=False, blank=False, related_name='contracts', on_delete=models.CASCADE,
                             verbose_name='Cliente asociado al contrato')
    car = models.ForeignKey(CarModel, null=False, blank=False, related_name='contracts', on_delete=models.CASCADE,
                            verbose_name='Modelo de coche asociado al contrato')

    creation_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                             verbose_name='Fecha de creación')
    modification_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                                 verbose_name='Fecha de modificación')

    def __str__(self):
        return f'Contrato asociado al usuario {self.user.first_name} y al modelo {self.car.name}'


class Fine(models.Model):
    id = models.AutoField(primary_key=True)
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    cost = models.IntegerField(null=False, verbose_name='Coste de la multa')
    description = models.CharField(max_length=30, null=False, blank=False,
                                   verbose_name='Texto descriptivo de la incidencia')
    pay_date = models.DateField(null=True, blank=True, verbose_name='Fecha de pago')

    contract = models.OneToOneField(Contract, null=False, blank=False, related_name='fine', on_delete=models.CASCADE,
                                    verbose_name='Contrato asociado a la multa')

    creation_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                             verbose_name='Fecha de creación')
    modification_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                                 verbose_name='Fecha de modificación')

    def __str__(self):
        return f'Multa asociada al contrato {self.contract}'
