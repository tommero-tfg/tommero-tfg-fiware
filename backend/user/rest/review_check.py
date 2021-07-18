import json

import requests
from rest_framework import viewsets
from rest_framework.response import Response


class ReviewCheckViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        user = request.user
        reviews_policy = self.user_privacy(user)
        response = {
            'reviewsPolicy': reviews_policy
        }
        return Response(data=response)

    def update(self, request, pk=None):
        user = request.user
        headers = {'Content-Type': 'text/plain'}
        url = f'http://fiware-orion:1026/v2/entities/urn:ngsi-ld:Privacy:{user.id}/attrs/reviewsPolicy/value?type=Privacy'
        requests.put(url, headers=headers, data=str(request.data['reviewPermission']))
        return Response(data=request.data['reviewPermission'])

    @staticmethod
    def user_privacy(user):
        url = f'http://fiware-orion:1026/v2/entities/urn:ngsi-ld:Privacy:{user.id}'
        fiware_response = requests.get(url)
        # noinspection PyTypeChecker
        return json.loads(fiware_response.text)['reviewsPolicy']['value'] == 'True' or \
               json.loads(fiware_response.text)['reviewsPolicy']['value'] == 'true'or \
               json.loads(fiware_response.text)['reviewsPolicy']['value'] == True
