from fastapi import APIRouter
from pydantic.types import UUID

from core import crud
from core.schemas import Route, WayPoint, LongestPaths
from core.crud import get_calculated_route_data

router = APIRouter(
    prefix="/route",
    tags=["route"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=201)
def create_route(route: Route):
    crud.create_route(route_id=route.route_id)
    return {"message": "success"}


@router.post("/{route_id}/way_point/", status_code=201)
def add_way_point(route_id: UUID, way_point: WayPoint):
    crud.add_way_point_to_route(
        route_id=route_id,
        lat=way_point.lat,
        lon=way_point.lon,
    )
    return {"message": "success"}


@router.get("/{route_id}/length/")
def calculate_length(route_id: UUID):
    route = get_calculated_route_data(route_id=route_id)
    length_km = route.length_km
    return {"km": length_km}


@router.get("/{route_id}/longest_paths/", response_model=LongestPaths)
def calculate_longest_paths(route_id: UUID):
    route = get_calculated_route_data(route_id=route_id)
    return {"longest_paths": route.longest_paths}
