import datetime
import json

import requests
from django_filters import rest_framework
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response

from ..models import ModelReview, CarModel


class ModelReviewSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.first_name')
    first_surname = serializers.CharField(source='user.user_info.first_surname')
    car = serializers.SlugRelatedField(slug_field='name', many=False, read_only=True)

    class Meta:
        model = ModelReview
        fields = ['guid', 'text', 'name', 'car', 'first_surname', 'creation_datetime']


class ModelReviewViewSet(viewsets.ModelViewSet):
    lookup_field = 'guid'
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ('car__guid',)
    serializer_class = ModelReviewSerializer

    def get_queryset(self):
        queryset = ModelReview.objects.all()
        car_guid = self.request.query_params.get('car__guid')
        if car_guid:
            queryset = queryset.filter(car__guid=car_guid)
        return queryset

    def list(self, request, *args, **kwargs):
        if request.query_params.get('user__guid'):
            guid = request.user.user_info.guid
            serializer = self.get_serializer(self.get_queryset().filter(user__user_info__guid=guid), many=True)
            return Response(serializer.data)
        reviews_allowed = [review for review in self.get_queryset() if self.user_privacy(review.user)]
        serializer = self.get_serializer(reviews_allowed, many=True)
        return Response(serializer.data)

    @staticmethod
    def user_privacy(user):
        url = f'http://fiware-orion:1026/v2/entities/urn:ngsi-ld:Privacy:{user.id}'
        fiware_response = requests.get(url)
        # noinspection PyTypeChecker
        return json.loads(fiware_response.text)['reviewsPolicy']['value'] == 'True' or \
               json.loads(fiware_response.text)['reviewsPolicy']['value'] == 'true' or \
               json.loads(fiware_response.text)['reviewsPolicy']['value'] == True

    def create(self, request, *args, **kwargs):
        car = CarModel.objects.get(guid=request.data['car_guid'])
        review = ModelReview.objects.create(text=request.data['review_message'], user_id=request.user.id,
                                            car_id=car.id, creation_datetime=datetime.date.today().isoformat())
        response = {'text': review.text, 'name': review.user.first_name,
                    'first_surname': review.user.user_info.first_surname, 'creation_datetime': review.creation_datetime}
        return Response(response, status=status.HTTP_201_CREATED)
