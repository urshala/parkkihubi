from django.db import models
from django.contrib.gis.db import models as gis_models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _

from .constants import WGS_84_SRID
from .mixins import TimestampedModelMixin, UUIDPrimaryKeyMixin


class PaymentZone(TimestampedModelMixin, UUIDPrimaryKeyMixin):
    number = models.IntegerField(verbose_name=_('zone number'), validators=[
        MinValueValidator(1), MaxValueValidator(3)])
    name = models.CharField(max_length=40, verbose_name=_('name'))
    geom = gis_models.MultiPolygonField(
        srid=WGS_84_SRID, verbose_name=_('geometry'))

    def __str__(self):
        return self.name
