import factory

from parkings.models import Permit, PermitSeries
from parkings.tests.utils import generate_areas, generate_subjects, generate_external_ids


class PermitSeriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PermitSeries


class PermitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permit

    series = factory.SubFactory(PermitSeriesFactory)
    external_id = factory.LazyFunction(lambda: generate_external_ids())
    subjects = factory.LazyFunction(lambda: generate_subjects(count=2))
    areas = factory.LazyFunction(lambda: generate_areas(count=3))


class ActivePermitFactory(PermitFactory):
    series = factory.LazyFunction(lambda: PermitSeriesFactory(active=True))
