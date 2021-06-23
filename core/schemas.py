from decimal import Decimal
from pydantic import BaseModel, Field
from pydantic.types import UUID
from typing import List


class Route(BaseModel):
    route_id: UUID

    class Config:
        schema_extra = {
            "example": {
                "route_id": "e84fee1e-fd4f-40f6-85b5-52ff46cbbb6e",
            }
        }


class WayPoint(BaseModel):
    lat: Decimal = Field(ge=-90, le=90)
    lon: Decimal = Field(ge=-180, le=180)

    class Config:
        schema_extra = {
            "example": {
                "lat": "59.23425",
                "lon": "18.23526",
            }
        }


class Length(BaseModel):
    km: Decimal

    class Config:
        schema_extra = {
            "example": {
                "km": "334.83",
            }
        }


class LongestPath(BaseModel):
    km: Decimal
    start: WayPoint
    stop: WayPoint

    class Config:
        schema_extra = {
            "example": {
                "km": "0",
                "start": {
                    "lat": "59.23425",
                    "lon": "18.23526",
                },
                "stop": {
                    "lat": "59.23425",
                    "lon": "18.23526",
                },
            }
        }


class LongestPaths(BaseModel):
    longest_paths: List[LongestPath]

    class Config:
        schema_extra = {
            "example": {
                "longest_paths": [
                    {
                        "km": "0",
                        "start": {
                            "lat": "59.23425",
                            "lon": "18.23526",
                        },
                        "stop": {
                            "lat": "59.23425",
                            "lon": "18.23526",
                        },
                    },
                    {
                        "km": "0",
                        "start": {
                            "lat": "59.23425",
                            "lon": "18.23526",
                        },
                        "stop": {
                            "lat": "59.23425",
                            "lon": "18.23526",
                        },
                    },
                ],
            }
        }
