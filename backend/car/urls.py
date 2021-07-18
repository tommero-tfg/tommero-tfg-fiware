from rest_framework import routers

from .rest import CarModelViewSet, ModelReviewViewSet, FilterViewSet

router = routers.DefaultRouter()

router.register(r'carmodel', CarModelViewSet, base_name='CarModel')
router.register(r'review', ModelReviewViewSet, base_name='ModelReview')
router.register(r'filter', FilterViewSet, base_name='Filters')
