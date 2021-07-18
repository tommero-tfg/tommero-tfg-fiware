from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import CarModel


class FilterViewSet(viewsets.ViewSet):
    def list(self, request):
        models = CarModel.objects.all()
        brands = set(model.brand for model in models)
        colors = set(image.name for model in models for image in model.images.all() if image.name)
        prices = [model.base_price for model in models]
        response = {
            'brands': brands,
            'colors': colors,
            'rangePrices': (min(prices), max(prices))
        }
        return Response(status=status.HTTP_200_OK, data=response)
