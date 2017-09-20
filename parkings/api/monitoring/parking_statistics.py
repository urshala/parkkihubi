import datetime

import pytz
from dateutil.parser import parse as parse_datetime
from django.db.models import Count, functions
from django.utils import timezone
from rest_framework import serializers, viewsets
from rest_framework.exceptions import ValidationError

from parkings.models import Parking, ParkingArea
from parkings.pagination import Pagination

from ..common import WGS84InBBoxFilter
from .permissions import MonitoringApiPermission


class ParkingStatisticsSerializer(serializers.Serializer):
    time = serializers.DateTimeField()
    zone = serializers.IntegerField(required=False)
    region = serializers.UUIDField(required=False)
    count = serializers.SerializerMethodField()

    def get_count(self, data):
        return data['count']


class ParkingStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [MonitoringApiPermission]
    queryset = ParkingArea.objects.all()
    serializer_class = ParkingStatisticsSerializer
    pagination_class = Pagination
    bbox_filter_field = 'geom'
    filter_backends = (WGS84InBBoxFilter,)
    bbox_filter_include_overlapping = True

    def get_queryset(self):
        (start, end, truncate_time, tz) = self._parse_query_params()
        return self._get_parkings_by_params(start, end, truncate_time, tz)

    def _parse_query_params(self):
        params = self.request.query_params
        now = timezone.now()
        monthago = now - datetime.timedelta(days=30)
        start = parse_time(params.get('start')) or monthago
        end = parse_time(params.get('end')) or now
        truncate_time = parse_resolution(params.get('resolution', 'hour'))
        tz = parse_timezone(params.get('tz'))
        return (start, end, truncate_time, tz)

    def _get_parkings_by_params(self, start, end, truncate_time, tz):
        parkings = Parking.objects.filter(
            time_start__gte=start, time_start__lt=end)

        return parkings.values(
            'region',
            time=truncate_time('time_start', tzinfo=tz),
        ).annotate(count=Count('pk')).order_by('time')


def parse_time(time_str):
    try:
        return parse_datetime(time_str) if time_str else None
    except ValueError:
        raise ValidationError("Invalid time: {!r}".format(time_str))


def parse_resolution(string):
    try:
        return _truncate_functions[string]
    except KeyError:
        raise ValidationError("Invalid resolution: {!r}".format(string))


_truncate_functions = {
    'year': functions.TruncYear,
    'month': functions.TruncMonth,
    'day': functions.TruncDay,
    'hour': functions.TruncHour,
    'minute': functions.TruncMinute,
    'second': functions.TruncSecond,
}


def parse_timezone(timezone_string, default='Europe/Helsinki'):
    try:
        return pytz.timezone(timezone_string or default)
    except pytz.UnknownTimeZoneError:
        raise ValueError("Unknown timezone: {!r}".format(timezone_string))
