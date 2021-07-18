from rest_framework import routers

from .rest import ContractViewSet
from .rest import FineViewSet

router = routers.DefaultRouter()

router.register(r'management/contract', ContractViewSet, base_name='contract')
router.register(r'management/fine', FineViewSet, base_name='fine')
