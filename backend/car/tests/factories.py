import uuid

import factory.fuzzy

from ..models import CarModel, CarImage, ModelReview
from user.tests.factories import UserFactory


class CarModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarModel
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n + 1000)
    guid = factory.LazyAttribute(lambda obj: uuid.uuid4)

    name = factory.LazyAttribute(lambda obj: 'Nombre de modelo {}'.format(obj.id))
    brand = factory.LazyAttribute(lambda obj: 'Marca de modelo {}'.format(obj.id))
    fuel = factory.LazyAttribute(lambda x: 'E')
    transmission = factory.LazyAttribute(lambda x: 'A')
    motor = factory.fuzzy.FuzzyInteger(low=70, high=150)
    seats = factory.fuzzy.FuzzyInteger(low=2, high=7)
    average_consumption = factory.fuzzy.FuzzyFloat(low=5.0, high=11.0, precision=2)
    price = factory.fuzzy.FuzzyInteger(low=20000, high=300000)
    release_year = factory.LazyAttribute(lambda x: '2021')


class ModelReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ModelReview
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n + 1000)
    guid = factory.LazyAttribute(lambda obj: uuid.uuid4)

    text = factory.LazyAttribute(lambda obj: 'Reseña num {}'.format(obj.id))

    user = factory.SubFactory(UserFactory)
    car = factory.SubFactory(CarModelFactory)


class CarImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarImage
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n + 1000)
    guid = factory.LazyAttribute(lambda obj: uuid.uuid4)
    car = factory.SubFactory(CarModelFactory)
