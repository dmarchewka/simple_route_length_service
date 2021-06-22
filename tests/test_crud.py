import datetime
from decimal import Decimal

import pytest
from freezegun import freeze_time

from core.crud import (
    create_route,
    add_way_point_to_route,
    calculate_paths_for_route,
    calculate_route_length_and_longest_paths,
)
from core.database import get_routes_db, reset_routes_db
from core.excpetions import RouteException
from core.models import Path, WayPoint


@pytest.fixture(autouse=True)
def clear_routes_db():
    reset_routes_db()


@freeze_time("2021-01-01 12:00:00")
def test_create_route():
    create_route("e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e")
    routes_db = get_routes_db()
    route = routes_db.get("e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e")

    today = datetime.date.today()

    assert route.route_id == "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"
    assert route.created == today
    assert route.length_km == 0
    assert route.way_points == []
    assert route.paths == []


def test_create_route__already_exists():
    create_route("e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e")
    with pytest.raises(ValueError):
        create_route("e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e")


D = Decimal


@freeze_time("2021-01-01 12:00:00")
def test_add_way_point_to_route():
    def check_way_point(way_point, lat, lon):
        assert way_point.lat == lat
        assert way_point.lon == lon
        assert way_point.created == datetime.datetime.now()

    uuid_1 = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"
    uuid_2 = "e84fee1e-fd4f-40f6-85b5-52ff46cccc6e"
    create_route(uuid_1)
    create_route(uuid_2)

    data = [
        (uuid_1, D("11.11"), D("0.13")),
        (uuid_2, D("50.11"), D("20.13")),
        (uuid_1, D("50.11"), D("20.13")),
        (uuid_1, D("44.11"), D("15.13")),
        (uuid_1, D("44.11"), D("15.13")),
    ]

    for uuid, lat, lon in data:
        add_way_point_to_route(uuid, lat, lon)

    routes_db = get_routes_db()
    route_1 = routes_db.get(uuid_1)
    route_2 = routes_db.get(uuid_2)
    assert len(route_1.way_points) == 4
    assert len(route_2.way_points) == 1

    for index, (lat, lon) in enumerate(
        [
            (D("11.11"), D("0.13")),
            (D("50.11"), D("20.13")),
            (D("44.11"), D("15.13")),
            (D("44.11"), D("15.13")),
        ]
    ):
        check_way_point(route_1.way_points[index], lat, lon)

    check_way_point(route_2.way_points[0], D("50.11"), D("20.13"))


def test_add_way_point_to_route__route_does_not_exist():
    with pytest.raises(ValueError):
        add_way_point_to_route(
            "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e", D("50.11"), D("20.13")
        )


@pytest.mark.parametrize(
    "lat, lon",
    [
        (D("150.11"), D(" 20.13")),
        (D("  90.1"), D(" 20.13")),
        (D(" -90.1"), D(" 20.13")),
        (D("  89.0"), D(" 180.1")),
        (D("  89.0"), D("-180.1")),
    ],
)
def test_add_way_point_to_route__invalid_input(lat, lon):
    uuid = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"
    create_route(uuid)
    with pytest.raises(AssertionError):
        add_way_point_to_route(uuid, lat, lon)


def test_add_way_point_to_route__old_route():
    uuid = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"
    with freeze_time("2021-01-01 12:00:00"):
        create_route(uuid)
    with pytest.raises(RouteException):
        add_way_point_to_route(uuid, D("50.11"), D("20.13"))


def test_calculate_paths_for_route():
    def check_path(path, start_lat, start_lon, stop_lat, stop_lon, length_km):
        assert path.length_km == length_km
        assert path.start.lat == start_lat
        assert path.start.lon == start_lon
        assert path.stop.lat == stop_lat
        assert path.stop.lon == stop_lon

    uuid = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"
    with freeze_time("2021-01-01 12:00:00"):
        create_route(uuid)
        for lat, lon in [
            (D("11.11"), D("0.13")),
            (D("50.11"), D("20.13")),
            (D("44.11"), D("15.13")),
            (D("44.11"), D("15.13")),
        ]:
            add_way_point_to_route(uuid, lat, lon)

    calculate_paths_for_route(uuid)
    route = get_routes_db().get(uuid)

    expected = [
        # start_lat, start_lon, stop_lat, stop_lon, length_km
        (D("11.11"), D("0.13"), D("50.11"), D("20.13"), D("4697.898349346")),
        (D("50.11"), D("20.13"), D("44.11"), D("15.13"), D("767.019406402")),
        (D("44.11"), D("15.13"), D("44.11"), D("15.13"), D("0")),
    ]

    for index, path in enumerate(route.paths):
        check_path(path, *expected[index])


def test_calculate_paths_for_route__route_not_exist():
    with pytest.raises(ValueError) as err:
        calculate_paths_for_route("e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e")
        assert err.value == "Route does not exist!"


def test_calculate_paths_for_route__route_open():
    uuid = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"
    create_route(uuid)
    with pytest.raises(RouteException) as err:
        calculate_paths_for_route(uuid)
        assert err.value == "This route is still open!"


def test_calculate_paths_for_route__already_calculated():
    uuid = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"
    with freeze_time("2021-01-01 12:00:00"):
        create_route(uuid)
    routes_db = get_routes_db()
    route = routes_db.get(uuid)
    route.paths.append(Path(length_km=D("0"), start=None, stop=None))
    with pytest.raises(RouteException) as err:
        calculate_paths_for_route(uuid)
        assert err.value == "Paths are already calculated!"


def test_calculate_paths_for_route__not_enough_way_points():
    uuid = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"
    with freeze_time("2021-01-01 12:00:00"):
        create_route(uuid)
    routes_db = get_routes_db()
    route = routes_db.get(uuid)
    route.way_points.append(WayPoint(lat=D("11.11"), lon=D("0.13")))

    with pytest.raises(ValueError) as err:
        calculate_paths_for_route(uuid)
        assert err.value == "Not enough way points in this route!"


def test_calculate_route_length_and_longest_paths():
    uuid = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"
    with freeze_time("2021-01-01 12:00:00"):
        create_route(uuid)
        for lat, lon in [
            (D("50.11"), D("20.13")),
            (D("11.11"), D("0.13")),
            (D("50.11"), D("20.13")),
            (D("44.11"), D("15.13")),
            (D("44.11"), D("15.13")),
        ]:
            add_way_point_to_route(uuid, lat, lon)

    calculate_paths_for_route(uuid)
    calculate_route_length_and_longest_paths(uuid)
    route = get_routes_db().get(uuid)

    assert route.length_km == D("10162.816105094")
    assert len(route.longest_paths) == 2

    assert route.longest_paths[0].length_km == D('4697.898349346')
    assert route.longest_paths[0].start == route.way_points[0]
    assert route.longest_paths[0].stop == route.way_points[1]

    assert route.longest_paths[1].length_km == D('4697.898349346')
    assert route.longest_paths[1].start == route.way_points[1]
    assert route.longest_paths[1].stop == route.way_points[2]


def test_calculate_route_length_and_longest_paths__route_not_exist():
    with pytest.raises(ValueError) as err:
        calculate_route_length_and_longest_paths("e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e")
        assert err.value == "Route does not exist!"


def test_calculate_route_length_and_longest_paths__route_open():
    uuid = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"
    create_route(uuid)
    with pytest.raises(RouteException) as err:
        calculate_route_length_and_longest_paths(uuid)
        assert err.value == "This route is still open!"


def test_calculate_route_length_and_longest_paths__path_not_calculated():
    uuid = "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e"
    with freeze_time("2021-01-01 12:00:00"):
        create_route(uuid)

    with pytest.raises(RouteException) as err:
        calculate_route_length_and_longest_paths(uuid)
        assert err.value == "You need to calculate paths first!"
