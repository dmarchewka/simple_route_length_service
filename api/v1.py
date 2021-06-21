from fastapi import APIRouter
from pydantic.types import UUID

from core.schemas import Route

router = APIRouter(
    prefix="/route",
    tags=["route"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=201)
def create_route(route: Route):
    print("test")
    return route


@router.post("/{route_id}/way_point/", status_code=201)
def add_way_point(route_id: UUID):
    # coordinates = request.get_json()  # {“lat”: 59.23425, “lon”: 18.23526}
    # assert 'lat' in coordinates
    # assert 'lon' in coordinates
    return {}


@router.get("/{route_id}/length/")
def calculate_length(route_id: UUID):
    return {}
