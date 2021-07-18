from unittest import TestCase

from .factories import *


class TestFactories(TestCase):
    """
    Tests for all functions that perform aggregations over the retail models.
    """

    def test_user_factory(self):
        UserFactory()

    def test_user_info_factory(self):
        UserInfoFactory()

