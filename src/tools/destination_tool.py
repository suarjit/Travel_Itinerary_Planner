
import requests
import time

# OpenStreetMap service configuration
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter"
]

HEADERS = {
    "User-Agent": "TravelItineraryPlanner/1.0 (educational project)"
}

def search_destination(destination):
    """
    Find the geographical location of a destination.
    """

    if not destination or not destination.strip():
        raise ValueError("Please provide a destination name.")

    params = {
        "q": destination,
        "format": "jsonv2",
        "limit": 1
    }

    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()
    results = response.json()

    if not results:
        return None

    place = results[0]

    return {
        "name": place.get("name", destination),
        "display_name": place.get("display_name"),
        "latitude": float(place["lat"]),
        "longitude": float(place["lon"])
    }


def find_attractions(latitude, longitude, radius=5000):
    """
    Find nearby tourist attractions using OpenStreetMap.
    Retries each server twice before trying the next server.
    """

    query = f"""
    [out:json][timeout:30];
    (
      node["tourism"~"attraction|museum|viewpoint|zoo"](around:{radius},{latitude},{longitude});
      way["tourism"~"attraction|museum|viewpoint|zoo"](around:{radius},{latitude},{longitude});
      relation["tourism"~"attraction|museum|viewpoint|zoo"](around:{radius},{latitude},{longitude});
      node["historic"](around:{radius},{latitude},{longitude});
    );
    out center tags;
    """

    last_error = None

    for url in OVERPASS_URLS:

        for attempt in range(1, 3):

            try:
                print(
                    f"Trying server: {url} "
                    f"(Attempt {attempt}/2)"
                )

                response = requests.post(
                    url,
                    data={"data": query},
                    headers=HEADERS,
                    timeout=40
                )

                response.raise_for_status()
                data = response.json()

                attractions = []

                for element in data.get("elements", []):
                    tags = element.get("tags", {})
                    name = tags.get("name")

                    if not name:
                        continue

                    attractions.append({
                        "name": name,
                        "category": (
                            tags.get("tourism")
                            or tags.get("historic")
                            or "attraction"
                        ),
                        "latitude": element.get(
                            "lat",
                            element.get("center", {}).get("lat")
                        ),
                        "longitude": element.get(
                            "lon",
                            element.get("center", {}).get("lon")
                        )
                    })

                print("Attraction search successful!")
                return attractions[:15]

            except (requests.RequestException, ValueError) as error:
                last_error = error
                print(f"Attempt failed: {error}")

                if attempt < 2:
                    print("Retrying in 3 seconds...")
                    time.sleep(3)

    raise RuntimeError(
        f"All Overpass servers failed. Last error: {last_error}"
    )

def research_destination(destination):
    """
    Main destination research tool.
    Uses cached attraction data if Overpass servers fail.
    """

    location = search_destination(destination)

    if location is None:
        return {
            "success": False,
            "message": "Destination not found."
        }

    try:
        attractions = find_attractions(
            location["latitude"],
            location["longitude"]
        )

        data_source = "OpenStreetMap Live API"
        cached = False

    except RuntimeError as error:

        print(f"Live API unavailable: {error}")
        print("Checking offline cache...")

        import json
        import os

        cache_file = os.path.join(
            "data",
            "cache",
            "darjeeling.json"
        )

        if (
            destination.lower().find("darjeeling") == -1
            or not os.path.exists(cache_file)
        ):
            return {
                "success": False,
                "message": "Live API unavailable and no matching cache found."
            }

        with open(cache_file, "r", encoding="utf-8") as file:
            cached_data = json.load(file)

        attractions = cached_data["attractions"]
        data_source = cached_data["source"]
        cached = True

    return {
        "success": True,
        "destination": location,
        "attractions": attractions,
        "total_attractions": len(attractions),
        "data_source": data_source,
        "cached": cached
    }