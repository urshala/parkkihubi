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


class PermitSerializer(serializers.ModelSerializer):
    def __init__(self, many=True, *args, **kwargs):
        super().__init__(many=many, *args, **kwargs)

    def create(self, validated_data):
        permits = [Permit(**item) for item in validated_data]
        return Permit.objects.bulk_create(permits)

    class Meta:
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
