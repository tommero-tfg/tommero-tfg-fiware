from rest_framework import viewsets, serializers

from ..models import CarModel, CarImage


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['name', 'color', 'image']


class CarModelSerializer(serializers.ModelSerializer):
    fuel = serializers.SerializerMethodField(method_name='get_fuel')
    transmission = serializers.SerializerMethodField(method_name='get_transmission')
    images = CarImageSerializer(read_only=True, many=True)

    @staticmethod
    def get_fuel(obj):
        return obj.get_fuel_display()

    @staticmethod
    def get_transmission(obj):
        return obj.get_transmission_display()

    class Meta:
        model = CarModel
        fields = ['guid', 'name', 'brand', 'fuel', 'transmission', 'motor', 'seats',
                  'average_consumption', 'base_price', 'images']


class CarModelListSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(method_name='get_date')
    images = CarImageSerializer(read_only=True, many=True)
    colors_associated = serializers.SerializerMethodField(method_name='get_colors_associated')

    @staticmethod
    def get_date(obj):
        return str(obj.creation_datetime.isoformat)

    @staticmethod
    def get_colors_associated(obj):
        return set(image.name for image in obj.images.all())

    class Meta:
        model = CarModel
        fields = ['guid', 'name', 'base_price', 'brand', 'images', 'colors_associated', 'date', 'creation_datetime']


class CarModelViewSet(viewsets.ModelViewSet):
    lookup_field = 'guid'
    queryset = CarModel.objects.all().order_by('creation_datetime')

    def get_serializer_class(self):
        if self.action == 'list':
            return CarModelListSerializer
        else:
            return CarModelSerializer
