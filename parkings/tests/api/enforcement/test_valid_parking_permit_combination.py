from datetime import datetime

import pytz
from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from parkings.factories.parking_area import generate_multi_polygon
from parkings.models import PermitArea

list_url = reverse("enforcement:v1:valid_parking_permit-list")


def list_url_for(reg_num):
    return "{url}?reg_num={reg_num}".format(url=list_url, reg_num=reg_num)


def _change_permit_series_owner_to(permit_series, staff_user):
    permit_series.owner = staff_user
    permit_series.save()


def test_endpoint_returns_valid_parking(staff_api_client, parking):
    reg_num = parking.registration_number

    response = staff_api_client.get(list_url_for(reg_num))
    json_response = response.json()

    assert response.status_code == HTTP_200_OK
    assert json_response["count"] == 1
    assert json_response["results"][0]["registration_number"] == reg_num


def test_endpoint_returns_valid_permit(
    staff_api_client, permit, staff_user, operator_factory
):
    operator_factory(user=staff_user)
    PermitArea.objects.all().update(permitted_user=staff_user)

    _change_permit_series_owner_to(permit.series, staff_user)

    reg_num = permit.subjects[0]["registration_number"]
    response = staff_api_client.get(list_url_for(reg_num))
    json_response = response.json()

    assert response.status_code == HTTP_200_OK
    assert json_response["count"] == len(permit.areas)


def test_endpoint_returns_both_valid_parking_and_permit(
    staff_api_client, parking, permit, operator_factory, staff_user
):
    operator_factory(user=staff_user)
    PermitArea.objects.all().update(permitted_user=staff_user)
    _change_permit_series_owner_to(permit.series, staff_user)

    permit_reg_num = permit.subjects[0]["registration_number"]
    parking.registration_number = permit_reg_num
    parking.save()

    response = staff_api_client.get(list_url_for(permit_reg_num))
    json_response = response.json()

    assert response.status_code == HTTP_200_OK
    assert json_response["count"] == 4  # 3 permits and 1 parking


def test_enforcer_can_only_view_permit_that_have_permitarea_where_she_is_allowed(
    staff_api_client, permit, operator_factory, staff_user
):
    operator_factory(user=staff_user)
    first_area_identifier = permit.areas[0]["area"]
    PermitArea.objects.filter(identifier=first_area_identifier).update(
        permitted_user=staff_user
    )
    _change_permit_series_owner_to(permit.series, staff_user)
    reg_num = permit.subjects[0]["registration_number"]

    response = staff_api_client.get(list_url_for(reg_num))
    json_response = response.json()

    assert response.status_code == HTTP_200_OK
    assert json_response["count"] == 1
    assert json_response["results"][0]["registration_number"] == reg_num


def create_permit_area(permitted_user, identifier):
    PermitArea.objects.get_or_create(
        identifier=identifier,
        defaults={"geom": generate_multi_polygon(), "permitted_user": permitted_user},
    )


def test_enforcer_cannot_view_permit_that_have_permitarea_where_she_is_not_permitted(
    staff_api_client,
    staff_user,
    permit_factory,
    parking_factory,
    admin_user,
    operator_factory,
    history_parking_factory,
):
    reg_number = "ABC-123"
    create_permit_area(staff_user, "A")
    create_permit_area(admin_user, "B")

    subjects = [
        {
            "start_time": datetime(2020, 1, 1, 1, 0, 0, 0, pytz.utc).isoformat(),
            "end_time": datetime(2020, 1, 1, 2, 0, 0, 0, pytz.utc).isoformat(),
            "registration_number": reg_number,
        }
    ]

    staff_permitted_area = [
        {
            "start_time": datetime(2020, 1, 1, 1, 0, 0, 0, pytz.utc).isoformat(),
            "end_time": datetime(2020, 1, 1, 2, 0, 0, 0, pytz.utc).isoformat(),
            "area": "A",
        }
    ]

    admin_permitted_area = [
        {
            "start_time": datetime(2020, 1, 1, 1, 0, 0, 0, pytz.utc).isoformat(),
            "end_time": datetime(2020, 1, 1, 2, 0, 0, 0, pytz.utc).isoformat(),
            "area": "B",
        }
    ]

    operator_factory(user=staff_user)
    operator_factory(user=admin_user)

    permit1, permit2 = [
        permit_factory(subjects=subjects, areas=staff_permitted_area) for _ in range(2)
    ]  # permit whose area belongs to admin user
    permit3, permit4 = [
        permit_factory(subjects=subjects, areas=admin_permitted_area) for _ in range(2)
    ]  # permit whose area belongs to staff user

    staff_belonging_permit = [permit1, permit2]
    admin_belonging_permit = [permit3, permit4]

    for staff_permit in staff_belonging_permit:
        _change_permit_series_owner_to(staff_permit.series, staff_user)

    for admin_permit in admin_belonging_permit:
        _change_permit_series_owner_to(admin_permit.series, admin_user)

    parking_factory(registration_number=reg_number)  # valid parking
    history_parking_factory(registration_number=reg_number)  # expired parking
    parking_factory(registration_number="XYZ-789")  # parking with different reg number

    response = staff_api_client.get(list_url_for(reg_number))

    assert response.status_code == HTTP_200_OK
    assert response.json()["count"] == 3  # permit1, permit2 and valid_parking
