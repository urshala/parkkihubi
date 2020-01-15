from django.db import transaction
from rest_framework import mixins, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from ...models import Permit, PermitSeries
from ..common_permit import (
    ActivePermitByExternalIdViewSet, PermitSeriesViewSet,
    PermitViewSet)


class OperatorPermitViewSet(PermitViewSet):
    pass


class OperatorEnforcementActivePermitByExternalViewSet(ActivePermitByExternalIdViewSet):
    pass


class OperatorPermitSeriesPayload(serializers.Serializer):
    deactivate_others = serializers.BooleanField()
    deactivate_series = serializers.ListField(
                            child=serializers.IntegerField(),
                            allow_empty=False,
                            required=False,
                            default=[]
                        )


class OperatorPermitSeriesViewSet(mixins.DestroyModelMixin, PermitSeriesViewSet):
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        with transaction.atomic():
            obj_to_activate = self.get_object()
            old_actives = self.queryset.filter(active=True)

            # Always activate the specified permit series regardless of what to deactivate
            if not obj_to_activate.active:
                obj_to_activate.active = True
                obj_to_activate.save()

            deactivate_payload = OperatorPermitSeriesPayload(data=request.data)
            deactivate_payload.is_valid(raise_exception=True)
            validated_data = deactivate_payload.validated_data

            if validated_data['deactivate_others']:
                old_actives.exclude(pk=obj_to_activate.pk).update(active=False)
            else:
                ids_to_deactivate = validated_data['deactivate_series']
                old_actives.filter(id__in=ids_to_deactivate).exclude(pk=obj_to_activate.pk).update(active=False)

            prunable_series = PermitSeries.objects.prunable()
            Permit.objects.filter(series__in=prunable_series).delete()
            prunable_series.delete()

            return Response({'status': 'OK'})
