import django_filters
import rest_framework_gis.pagination as gis_pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from ...models import Parking
from ..common import WGS84InBBoxFilter
from .permissions import MonitoringApiPermission
from .serializers import ParkingSerializer


class ParkingFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Parking
        fields = {
            'region': ['exact'],
            'zone': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'time_start': ['lt', 'lte', 'gt', 'gte'],
            'time_end': ['lt', 'lte', 'gt', 'gte', 'isnull'],
        }
        strict = django_filters.STRICTNESS.RAISE_VALIDATION_ERROR


class ParkingViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [MonitoringApiPermission]
    queryset = Parking.objects.all().order_by('time_start')
    serializer_class = ParkingSerializer
    pagination_class = gis_pagination.GeoJsonPagination
    filter_class = ParkingFilter
    bbox_filter_field = 'location'
    filter_backends = [DjangoFilterBackend, WGS84InBBoxFilter]
    bbox_filter_include_overlapping = True
