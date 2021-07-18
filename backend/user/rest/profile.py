from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from user.models import UserInfo

from contract.models import Fine


class ProfileViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        user = request.user
        response = {
            'name': user.first_name,
            'firstSurname': user.user_info.first_surname,
            'secondSurname': user.user_info.second_surname,
            'email': user.email,
            'dni': user.user_info.dni,
            'birthdate': '/'.join(str(user.user_info.birthdate).split('-')[::-1]),
            'phoneNumber': user.user_info.phone_number,
        }
        return Response(data=response)

    def update(self, request, pk=None):
        user = request.user
        user_to_update = User.objects.get(user_info__guid=user.user_info.guid)
        user_info_to_update = UserInfo.objects.get(user__id=user.id)
        user_to_update.first_name = request.data['name']
        user_info_to_update.first_surname = request.data['firstSurname']
        user_info_to_update.second_surname = request.data['secondSurname']
        user_to_update.email = request.data['email']
        user_info_to_update.birthdate = '-'.join(request.data['birthdate'].split('/')[::-1])
        user_info_to_update.phone_number = request.data['phoneNumber']
        user_to_update.save()
        user_info_to_update.save()

        response = {
            'name': user_to_update.first_name,
            'firstSurname': user_to_update.user_info.first_surname,
            'secondSurname': user_to_update.user_info.second_surname,
            'email': user_to_update.email,
            'dni': user_to_update.user_info.dni,
            'birthdate': user_to_update.user_info.birthdate,
            'phoneNumber': user_to_update.user_info.phone_number,
        }

        return Response(data=response)

    def destroy(self, request, pk=None):
        active_contracts = request.user.contracts.filter(status='A')
        reject_contracts = request.user.contracts.filter(status='C')
        contract_ids_associated = [contract.id for contract in reject_contracts]
        reject_active = Fine.objects.filter(contract_id__in=contract_ids_associated, pay_date__isnull=True)
        user = User.objects.get(id=request.user.id)
        request.user.auth_token.delete()
        if active_contracts or reject_active:
            user.is_active = False
            user.save()
        else:
            user.delete()
        return Response(status=status.HTTP_200_OK)
