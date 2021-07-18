from unittest import TestCase

from .factories import *


class TestFactories(TestCase):
    """
    Tests for all functions that perform aggregations over the retail models.
    """

    def test_car_model_factory(self):
        CarModelFactory()

    def test_car_image_factory(self):
        CarImageFactory()

    def test_model_review_factory(self):
        ModelReviewFactory()

