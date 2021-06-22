import datetime
from decimal import Decimal
from uuid import UUID


class Route:
    def __init__(self, route_id: UUID):
        self.route_id = route_id
        self.created = datetime.date.today()
        self.length_km = 0
        self.way_points = []
        self.paths = []
        self.longest_paths = []


class WayPoint:
    def __init__(self, lat: Decimal, lon: Decimal):
        assert -90 <= lat <= 90
        assert -180 <= lon <= 180

        self.lat = lat
        self.lon = lon
        self.created = datetime.datetime.now()

    @property
    def coordinates(self):
        return self.lat, self.lon


class Path:
    def __init__(self, length_km: Decimal, start: WayPoint, stop: WayPoint):
        self.start = start
        self.stop = stop
        self.length_km = length_km
