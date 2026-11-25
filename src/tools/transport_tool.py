
from geopy.distance import geodesic

def calculate_distance(
    origin_lat,
    origin_lon,
    destination_lat,
    destination_lon
):
    """
    Calculate geographical distance between two locations.
    Returns distance in kilometres.
    """

    origin = (origin_lat, origin_lon)
    destination = (destination_lat, destination_lon)

    distance = geodesic(origin, destination).kilometers

    return round(distance, 2)

def estimate_travel_time(distance_km, transport_mode):
    """
    Estimate travel time based on transport mode.

    These are approximate average speeds, not live traffic data.
    """

    average_speeds = {
        "walking": 5,
        "car": 35,
        "bus": 30,
        "train": 45
    }

    mode = transport_mode.lower()

    if mode not in average_speeds:
        raise ValueError(
            "Unsupported mode. Choose walking, car, bus or train."
        )

    speed = average_speeds[mode]

    time_hours = distance_km / speed

    return round(time_hours * 60, 2)

def estimate_transport(
    origin_lat,
    origin_lon,
    destination_lat,
    destination_lon,
    transport_mode="car"
):
    """
    Main transport estimation tool.
    """

    distance = calculate_distance(
        origin_lat,
        origin_lon,
        destination_lat,
        destination_lon
    )

    travel_time = estimate_travel_time(
        distance,
        transport_mode
    )

    return {
        "success": True,
        "distance_km": distance,
        "transport_mode": transport_mode,
        "estimated_travel_time_minutes": travel_time,
        "average_speed_kmh": {
            "walking": 5,
            "car": 35,
            "bus": 30,
            "train": 45
        }[transport_mode.lower()],
        "note": "Approximate straight-line distance and travel time, not a verified route."
    }