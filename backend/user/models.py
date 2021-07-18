import uuid

from django.contrib.auth.models import User
from django.db import models


class UserInfo(models.Model):
    class Meta:
        verbose_name = 'UserInfo'

    id = models.AutoField(primary_key=True)
    guid = models.UUIDField(default=uuid.uuid4, editable=False)

    first_surname = models.CharField(max_length=64, null=True, blank=True, verbose_name='Primer apellido')
    second_surname = models.CharField(max_length=64, null=True, blank=True, verbose_name='Segundo apellido')
    dni = models.CharField(max_length=9, null=True, verbose_name='Documento de identificación nacional')
    phone_number = models.CharField(max_length=32, null=True, verbose_name='Número de teléfono')
    birthdate = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento del usuario')

    user = models.OneToOneField(User, null=False, blank=False, related_name='user_info', on_delete=models.CASCADE,
                                verbose_name='Usuario')

    creation_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                             verbose_name='Fecha de creación')
    modification_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                                 verbose_name='Fecha de modificación')

    def __str__(self):
        return f'Info of user {self.user.first_name}'


class Application(models.Model):
    id = models.AutoField(primary_key=True)
    guid = models.UUIDField(default=uuid.uuid4, editable=False)

    rights = models.FileField(upload_to='access_right/', null=True, blank=True)

    user_info = models.OneToOneField(UserInfo, null=False, blank=False, related_name='user_info',
                                     on_delete=models.CASCADE, verbose_name='Usuario')

    creation_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                             verbose_name='Fecha de creación')
    modification_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                                 verbose_name='Fecha de modificación')

    def __str__(self):
        return f'Application of user ({self.user_info.user.id})'
