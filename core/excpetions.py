class RouteException(Exception):
    """
    Raise when someone wants to modify routes that are closed,
    or create paths on an open route
    """
