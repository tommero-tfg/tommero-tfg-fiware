from rest_framework import viewsets, serializers, status
from rest_framework.response import Response

from ..models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    document = serializers.FileField(source='rights', use_url=True, allow_null=True)

    class Meta:
        model = Application
        fields = ['document']


class ApplicationViewSet(viewsets.ModelViewSet):
    lookup_field = 'guid'
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    http_method_names = ['get', 'list', 'post']

    def retrieve(self, request, *args, **kwargs):
        instance = Application.objects.filter(user_info_id=request.user.user_info.id, rights__isnull=False).first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, content_type='application/pdf')

    def create(self, request, *args, **kwargs):
        Application.objects.create(user_info_id=request.user.user_info.id)
        return Response(status=status.HTTP_200_OK)
