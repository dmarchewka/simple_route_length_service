from decimal import Decimal

import pytest

from core.models import WayPoint
from core.util import calculate_length_km


@pytest.mark.parametrize(
    "start_lat, start_lon, stop_lat, stop_lon, expected",
    [
        ("52.2296756", "21.0122287", "52.406374", "16.9251681", "279.352901604"),
        ("41.49008", "-71.312796", "41.499498", "-81.695391", "866.455432910"),
    ],
)
def test_calculate_length_km(start_lat, start_lon, stop_lat, stop_lon, expected):

    start = WayPoint(Decimal(start_lat), Decimal(start_lon))
    stop = WayPoint(Decimal(stop_lat), Decimal(stop_lon))

    result = calculate_length_km(start, stop)

    assert result == Decimal(expected)
