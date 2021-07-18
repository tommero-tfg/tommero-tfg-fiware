from rest_framework import viewsets, serializers, status
from rest_framework.response import Response

from ..models import Fine


class FineSerializer(serializers.ModelSerializer):
    contract = serializers.SlugRelatedField(slug_field='guid', many=False, read_only=True)

    class Meta:
        model = Fine
        fields = ('cost', 'description', 'pay_date', 'contract', 'creation_datetime',)


class FineViewSet(viewsets.ModelViewSet):
    lookup_field = 'guid'
    queryset = Fine.objects.all()
    serializer_class = FineSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        user = request.user
        contracts = Fine.objects.filter(contract__user__user_info__guid=user.user_info.guid)
        serializer = self.get_serializer(contracts, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
