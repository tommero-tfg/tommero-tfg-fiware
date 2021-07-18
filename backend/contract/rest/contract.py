from car.models import CarModel
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
import datetime

from .fine import FineSerializer
from ..models import Contract, Fine


class ContractSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(method_name='get_status')
    status_color = serializers.SerializerMethodField(method_name='get_status_color')
    car = serializers.SlugRelatedField(slug_field='name', many=False, read_only=True)

    @staticmethod
    def get_status(obj):
        return obj.get_status_display()

    @staticmethod
    def get_status_color(obj):
        status_color_by_tag = {
            'En proceso': 'blue',
            'Activo': 'green',
            'Finalizado': 'black',
            'Cancelado': 'red',
        }
        return status_color_by_tag[obj.get_status_display()]

    class Meta:
        model = Contract
        fields = ['guid', 'monthly_cost', 'annual_mileage', 'duration', 'start_date', 'reject_date', 'bank_account',
                  'status', 'status_color', 'user', 'car', 'car_color', 'creation_datetime']


class ContractViewSet(viewsets.ModelViewSet):
    lookup_field = 'guid'
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        duration_increment = {12: 1.3, 24: 1.2, 36: 1.1, 48: 1, 60: 1}
        km_increment = {15000: 1, 20000: 1, 25000: 1.1, 30000: 1.2, 35000: 1.3, 40000: 1.4, 45000: 1.5}
        user = request.user
        car = CarModel.objects.get(guid=request.data['carGuid'])
        price = car.base_price * duration_increment[request.data['duration']] * km_increment[request.data['km']]
        Contract.objects.create(monthly_cost=price, duration=request.data['duration'],
                                annual_mileage=request.data['km'], car_color=request.data['carColor'],
                                car_id=car.id, user_id=user.id, status='E', bank_account=request.data['account'])
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        user = request.user
        contracts = Contract.objects.filter(user__user_info__guid=user.user_info.guid)
        serializer = self.get_serializer(contracts, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        contract_to_delete = self.get_object()
        if contract_to_delete.status == 'E':
            contract_to_delete.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            contract_to_delete.status = 'C'
            contract_to_delete.reject_date = datetime.date.today()
            today = datetime.date.today()
            duration_to_end = (today.year - contract_to_delete.start_date.year) * 12 \
                              + today.month - contract_to_delete.start_date.month
            fine_price = duration_to_end * contract_to_delete.monthly_cost * 0.75
            fine = Fine.objects.create(description=request.query_params['description'],
                                       contract_id=contract_to_delete.id,
                                       cost=fine_price)
            contract_to_delete.save()
            serializer = {
                'description': fine.description,
                'cost': fine.cost,
                'creation_datetime': fine.creation_datetime,
                'contract': fine.contract.guid,
                'pay_date': ''
            }
            return Response(status=status.HTTP_200_OK, data=serializer)
