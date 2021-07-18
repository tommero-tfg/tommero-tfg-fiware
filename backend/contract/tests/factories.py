import uuid

import factory.fuzzy
from car.tests.factories import CarModelFactory
from user.tests.factories import UserFactory

from ..models import Contract, Fine


class ContractFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contract
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n + 1000)
    guid = factory.LazyAttribute(lambda obj: uuid.uuid4)

    monthly_cost = factory.fuzzy.FuzzyFloat(low=150.0, high=480.0, precision=2)
    annual_mileage = factory.fuzzy.FuzzyInteger(low=15000, high=40000)
    duration = factory.fuzzy.FuzzyInteger(low=12, high=40)
    start_date = factory.LazyAttribute(lambda x: '2021')
    reject_date = factory.LazyAttribute(lambda x: '2021')
    bank_account = factory.LazyAttribute(lambda obj: 'Marca de modelo {}'.format(obj.id))
    status = factory.LazyAttribute(lambda x: 'E')
    car_color = factory.LazyAttribute(lambda obj: 'Color {}'.format(obj.id))

    user = factory.SubFactory(UserFactory)
    car = factory.SubFactory(CarModelFactory)


class FineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Fine
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n + 1000)
    guid = factory.LazyAttribute(lambda obj: uuid.uuid4)

    cost = factory.fuzzy.FuzzyInteger(low=700, high=15000)
    description = brand = factory.LazyAttribute(lambda obj: 'Descripcion {}'.format(obj.id))
    pay_date = factory.LazyAttribute(lambda x: '2021')
    contract = factory.SubFactory(ContractFactory)
