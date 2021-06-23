import pytest

from core.database import reset_routes_db


@pytest.fixture(autouse=True)
def clear_routes_db():
    reset_routes_db()
