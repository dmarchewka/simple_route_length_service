import datetime
import itertools
from decimal import Decimal
from uuid import UUID


class Route:

    def __init__(self, route_id: UUID):
        self.route_id = route_id
        self.route_id = datetime.date.today()


class WayPoint:
    id_iter = itertools.count()

    def __init__(self, lat: Decimal, lon: Decimal):
        self.id = next(self.id_iter)
        self.lat = lat
        self.lon = lon
        self.datetime = datetime.datetime.now()


class Path:

    def __init__(self, start: WayPoint, stop: WayPoint):
        self.start = start
        self.stop = stop
        self.length_km = 0
