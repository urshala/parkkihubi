from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, serializers, viewsets

from ...models import Permit, PermitSeries


class PermitSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermitSeries
        fields = ['id', 'active']


class PermitSeriesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = PermitSeries.objects.all()
    serializer_class = PermitSeriesSerializer


class PermitListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        permits = [Permit(**item) for item in validated_data]
        return Permit.objects.bulk_create(permits)


class PermitSerializer(serializers.ModelSerializer):
    subjects = serializers.ListField(
        child=serializers.CharField(max_length=20),
        max_length=40)

    areas = serializers.ListField(
        child=serializers.CharField(max_length=5),
        max_length=33)

    class Meta:
        list_serializer_class = PermitListSerializer
        model = Permit
        fields = [
            'id',
            'series',
            'start_time',
            'end_time',
            'subjects',
            'areas',
        ]


class PermitViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Permit.objects.all()
    serializer_class = PermitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['series']

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)
