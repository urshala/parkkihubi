from ...models import EnforcementDomain
from ..common_permit import (
    ActivePermitByExternalIdViewSet, PermitSerializer, PermitSeriesViewSet,
    PermitViewSet)


class EnforcementPermitSerializer(PermitSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['domain'].required = False

    def validate(self, data):
        # domain = self.context.request.user.enforcer.enforced_domain
        # TODO: Don't hard code it; instead get like the statement above
        data['domain'] = EnforcementDomain.objects.first()
        return data


class EnforcementPermitSeriesViewSet(PermitSeriesViewSet):
    pass


class EnforcementPermitViewSet(PermitViewSet):
    serializer_class = EnforcementPermitSerializer

    def _allowed_methods(self):
        allowed_methods = super()._allowed_methods()
        allowed_methods.remove('DELETE')
        return allowed_methods


class EnforcementActivePermitByExternalIdViewSet(
    ActivePermitByExternalIdViewSet
):
    pass
