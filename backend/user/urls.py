from rest_framework import routers

from .rest import ProfileViewSet, CreateUserViewSet, ReviewCheckViewSet, ApplicationViewSet

router = routers.DefaultRouter()

router.register(r'profile', ProfileViewSet, base_name='Profile')
router.register(r'createuser', CreateUserViewSet, base_name='CreateUser')
router.register(r'reviewcheck', ReviewCheckViewSet, base_name='ReviewCheck')
router.register(r'application', ApplicationViewSet, base_name='Application')
