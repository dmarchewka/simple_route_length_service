routes_db = None


def get_routes_db():
    global routes_db
    if not routes_db:
        routes_db = {}
    return routes_db


def reset_routes_db():
    global routes_db
    routes_db = {}
