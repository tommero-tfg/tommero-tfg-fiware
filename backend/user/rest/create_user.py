import datetime
import json

import requests
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import UserInfo


class CreateUserViewSet(viewsets.ViewSet):
    def create(self, request):
        user_input = request.data
        headers = {'Content-Type': 'application/json'}
        date = datetime.date.today().isoformat()

        try:
            with transaction.atomic():
                birthdate_args = user_input['birthDate'].split('/')
                birthdate = datetime.date(int(birthdate_args[2]), int(birthdate_args[1]), int(birthdate_args[0]))
                user = User.objects.create_user(username=user_input['username'], password=user_input['pass'],
                                                email=user_input['email'], first_name=user_input['name'])
                UserInfo.objects.create(first_surname=user_input['firstSurname'],
                                        second_surname=user_input['secondSurname'],
                                        dni=user_input['dni'], birthdate=birthdate,
                                        phone_number=user_input['phoneNumber'],
                                        user=user)

                entity_schema = {
                    "id": f"urn:ngsi-ld:Privacy:{user.id}",
                    "type": "Privacy",
                    "privacyPolicy": {
                        "type": "Text",
                        "value": f"{user_input['privacyPolicy']}",
                        "metadata": {
                            "dateCreated": {
                                "value": date,
                                "type": "DateTime"
                            }
                        }
                    },
                    "cookiesPolicy": {
                        "type": "Text",
                        "value": f"{user_input['cookiesPolicy']}",
                        "metadata": {
                            "dateCreated": {
                                "value": date,
                                "type": "DateTime"
                            }
                        }
                    },
                    "reviewsPolicy": {
                        "type": "Text",
                        "value": f"{user_input['reviewsPolicy']}",
                        "metadata": {
                            "dateCreated": {
                                "value": date,
                                "type": "DateTime"
                            },
                            "dateModified": {
                                "value": date,
                                "type": "DateTime"
                            }
                        }
                    }
                }

                entity = json.dumps(entity_schema)
                requests.post('http://fiware-orion:1026/v2/entities', data=entity, headers=headers)
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_200_OK)
