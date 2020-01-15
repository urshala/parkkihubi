from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from ..url_utils import versioned_url
from .parking import OperatorAPIParkingViewSet
from .enforcement_domain import EnforcementDomainView


class Router(DefaultRouter):
    def get_urls(self):
        urls = super().get_urls()
        return urls + [
            url(r"^enforcement_domain/$", EnforcementDomainView.as_view(), name="enforcement_domain")
        ]

    def get_api_root_view(self, *args, **kwargs):
        view = super().get_api_root_view(*args, **kwargs)
        view.initkwargs['api_root_dict']['enforcement_domain'] = 'enforcement_domain'
        return view


router = Router()
router.register(r'parking', OperatorAPIParkingViewSet)

app_name = 'operator'
urlpatterns = [
    versioned_url('v1', router.urls),
]
