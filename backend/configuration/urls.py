"""configuration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from car.urls import router as car_router
from contract.urls import router as contract_router
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from user.urls import router as user_router

from . import settings
from .view import Logout, CustomAuthToken

router = routers.DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(car_router.registry)
router.registry.extend(contract_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', CustomAuthToken.as_view()),
    url(r'^logout/', Logout.as_view()),
    url(r'^api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
