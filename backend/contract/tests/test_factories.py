from unittest import TestCase

from .factories import *


class TestFactories(TestCase):
    """
    Tests for all functions that perform aggregations over the retail models.
    """

    def test_contract_factory(self):
        ContractFactory()

    def test_fine_factory(self):
        FineFactory()

