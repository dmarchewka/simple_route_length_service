import datetime
from datetime import timedelta
from http import HTTPStatus
from uuid import UUID

from fastapi.testclient import TestClient
from freezegun import freeze_time

from core.database import get_routes_db
from core.models import Route
from main import app

client = TestClient(app)


def make_route_request(uuid: UUID = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"):
    return client.post("/route/", json={"route_id": uuid})


def make_add_way_point_request(
    uuid: UUID = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e",
    lat: str = "11.11",
    lon: str = "0.13",
):
    return client.post(
        f"/route/{uuid}/way_point/",
        json={
            "lat": lat,
            "lon": lon,
        },
    )


def make_calculate_length_request(uuid: UUID = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"):
    return client.get(f"/route/{uuid}/length/")


def make_calculate_longest_paths_request(
    uuid: UUID = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e",
):
    return client.get(f"/route/{uuid}/longest_paths/")


def test_create_route():
    response = make_route_request()
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"message": "success"}


def test_create_route__already_exists():
    make_route_request()
    response = make_route_request()
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {"message": ["Route already exists!"]}


def test_add_way_point():
    make_route_request()
    response = make_add_way_point_request()
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"message": "success"}


def test_add_way_point__route_does_not_exist():
    response = make_add_way_point_request()
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {"message": ["Route does not already exist!"]}


def test_calculate_length():
    with freeze_time("2021-01-01 12:00:00"):
        make_route_request()
        for lat, lon in [
            ("-25.4025905", "-49.3124416"),
            (" -23.559798", "-46.634971"),
            (" 59.3258414", "17.70188"),
            ("  54.273901", "18.591889"),
        ]:
            make_add_way_point_request(lat=lat, lon=lon)
    response = make_calculate_length_request()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"km": 11794.389755872}


def test_calculate_longest_paths():
    with freeze_time("2021-01-01 12:00:00"):
        make_route_request()
        for lat, lon in [
            ("-25.4025905", "-49.3124416"),
            (" -23.559798", "-46.634971"),
            (" 59.3258414", "17.70188"),
            (" -23.559798", "-46.634971"),
            ("  54.273901", "18.591889"),
        ]:
            make_add_way_point_request(lat=lat, lon=lon)
    response = make_calculate_longest_paths_request()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "longest_paths": [
            {
                "km": 10889.633473117,
                "start": {"lat": -23.559798, "lon": -46.634971},
                "stop": {"lat": 59.3258414, "lon": 17.70188},
            },
            {
                "km": 10889.633473117,
                "start": {"lat": 59.3258414, "lon": 17.70188},
                "stop": {"lat": -23.559798, "lon": -46.634971},
            },
        ]
    }
