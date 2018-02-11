from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .parking import ParkingViewSet
from .region import RegionViewSet
from .region_statistics import RegionStatisticsViewSet
from .valid_parking import ValidParkingViewSet

router = DefaultRouter()
router.register(r'parking', ParkingViewSet, base_name='parking')
router.register(r'region', RegionViewSet, base_name='region')
router.register(r'region_statistics', RegionStatisticsViewSet,
                base_name='regionstatistics')
router.register(r'valid_parking', ValidParkingViewSet,
                base_name='valid_parking')

urlpatterns = [
    url(r'^', include(router.urls, namespace='v1')),
]
