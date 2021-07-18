import uuid

import factory.fuzzy
from django.contrib.auth.models import User

from ..models import UserInfo


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n + 1000)

    first_name = factory.LazyAttribute(lambda obj: 'Nombre  {}'.format(obj.id))
    email = factory.LazyAttribute(lambda obj: 'Email {}'.format(obj.id))
    username = factory.LazyAttribute(lambda obj: 'Nombre de usuario {}'.format(obj.id))
    is_active = bool(factory.fuzzy.FuzzyInteger(low=0, high=1))


class UserInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserInfo
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n + 1000)
    guid = factory.LazyAttribute(lambda obj: uuid.uuid4)

    first_surname = factory.LazyAttribute(lambda obj: 'Primer apellido {}'.format(obj.id))
    second_surname = factory.LazyAttribute(lambda obj: 'Segundo apellido {}'.format(obj.id))
    dni = factory.LazyAttribute(lambda obj: 'DNI {}'.format(obj.id))
    phone_number = factory.LazyAttribute(lambda obj: 'Numero de telefono {}'.format(obj.id))
    birthdate = factory.LazyAttribute(lambda obj: 'Cumple {}'.format(obj.id))
    user = factory.SubFactory(UserFactory)
