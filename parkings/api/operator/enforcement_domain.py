from rest_framework import generics, serializers

from parkings.models import EnforcementDomain


class EnforcementDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnforcementDomain
        fields = ("code", "name")


class EnforcementDomainView(generics.ListAPIView):
    serializer_class = EnforcementDomainSerializer
    queryset = EnforcementDomain.objects.all()
