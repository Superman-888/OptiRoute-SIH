import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS coordinates in kilometers.
    """

    earth_radius = 6371.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius * c


def calculate_route_distance(route, locations):
    """
    Calculate total distance for:

    Depot -> customers -> Depot

    route:
        [0, 3]

    locations:
        list of (latitude, longitude)
    """

    if not route:
        return 0.0

    total_distance = 0.0

    # Depot -> first customer
    previous = locations[0]

    for customer_index in route:
        current = locations[customer_index + 1]

        total_distance += haversine_distance(
            previous[0],
            previous[1],
            current[0],
            current[1]
        )

        previous = current

    # Last customer -> Depot
    depot = locations[0]

    total_distance += haversine_distance(
        previous[0],
        previous[1],
        depot[0],
        depot[1]
    )

    return total_distance