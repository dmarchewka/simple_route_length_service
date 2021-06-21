from decimal import Decimal, ROUND_HALF_UP

from geopy.distance import geodesic

from core.models import WayPoint


def calculate_length_km(start: WayPoint, stop: WayPoint) -> Decimal:
    distance = geodesic(start.coordinates, stop.coordinates)
    return round_(Decimal(distance.km))


def round_(value, decimal_places=9, rounding=ROUND_HALF_UP):
    assert isinstance(value, Decimal)
    return value.quantize(Decimal("10") ** (-decimal_places), rounding=rounding)
