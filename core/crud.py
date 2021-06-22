import datetime
from decimal import Decimal
from uuid import UUID

from core.database import get_routes_db
from core.excpetions import RouteException
from core.models import Route, WayPoint, Path
from core.util import calculate_length_km


def create_route(route_id: UUID):
    routes_db = get_routes_db()
    if route_id in routes_db:
        raise ValueError("Route already exists!")
    routes_db[route_id] = Route(route_id=route_id)


def add_way_point_to_route(route_id: UUID, lat: Decimal, lon: Decimal):
    assert -90 <= lat <= 90
    assert -180 <= lon <= 180

    route = get_routes_db().get(route_id)
    if not route:
        raise ValueError("Route does not already exist!")
    elif route.created != datetime.date.today():
        raise RouteException("This route is already closed!")

    route.way_points.append(
        WayPoint(
            lat=lat,
            lon=lon,
        )
    )


def calculate_paths_for_route(route_id: UUID):
    route = get_routes_db().get(route_id)

    if not route:
        raise ValueError("Route does not exist!")
    elif route.created == datetime.date.today():
        raise RouteException("This route is still open!")
    elif len(route.paths) > 0:
        raise RouteException("Paths are already calculated!")
    elif len(route.way_points) < 2:
        raise ValueError("Not enough way points in this route!")

    for i, start in enumerate(route.way_points[:-1]):
        stop = route.way_points[i + 1]
        length_km = calculate_length_km(start, stop)
        route.paths.append(
            Path(
                length_km=length_km,
                start=start,
                stop=stop,
            )
        )
