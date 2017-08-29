import datetime

import pytest
from django.contrib.gis.geos import Point
from django.test import override_settings
from django.utils.timezone import now, utc

from parkings.models import Operator, Parking


def test_operator_instance_creation():
    Operator(name="name", user_id=1)


def test_parking_instance_creation():
    Parking(
        location=Point(60.193609, 24.951394),
        operator_id=1,
        registration_number="ABC-123",
        time_end=now() + datetime.timedelta(days=1),
        time_start=now(),
        zone=3,
    )


@pytest.mark.django_db
@override_settings(TIME_ZONE='Europe/Helsinki')
def test_parking_str(parking_factory):
    parking = parking_factory(
        time_start=datetime.datetime(2014, 1, 1, 6, 0, 0, tzinfo=utc),
        time_end=datetime.datetime(2016, 1, 1, 7, 0, 0, tzinfo=utc),
        registration_number='ABC-123',
    )
    assert all(str(parking).count(val) == 1 for val in ('2014', '2016', '8', '9', 'ABC-123'))

    parking = parking_factory(
        time_start=datetime.datetime(2016, 1, 1, 6, 0, 0, tzinfo=utc),
        time_end=datetime.datetime(2016, 1, 1, 7, 0, 0, tzinfo=utc),
        registration_number='ABC-123',
    )
    assert all(str(parking).count(val) == 1 for val in ('2016', '8', '9', 'ABC-123'))

    parking = parking_factory(
        time_start=datetime.datetime(2016, 1, 1, 6, 0, 0, tzinfo=utc),
        time_end=None,
        registration_number='ABC-123',
    )
    assert all(str(parking).count(val) == 1 for val in ('2016', '8', 'ABC-123'))
